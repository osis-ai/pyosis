"""命令流 → pyosis 代码生成器.

按字段顺序生成调用, 支持:
  - direct: engine.method(args...)  (args=fields[skip:])
  - chain:  engine.get(fields[skip]).method(fields[rest_prefix] + fields[skip+1:]...)
  - matrix: *dim + 赋值 → engine.matrix(name, nested_list)
"""

from __future__ import annotations
from typing import List

from .matrix import MatrixAccumulator
from .parser import ParsedCommand
from .routes import ROUTES

_ROUTE_ALIASES = {
    "clear": "Clear",
    "clc": "Clc",
}

_LINE_I_NAMES = [
    "dOffsetXI", "dOffsetYI", "dOffsetZI",
    "dFXI", "dFYI", "dFZI", "dMXI", "dMYI", "dMZI",
]

_LINE_J_NAMES = [
    "dOffsetXJ", "dOffsetYJ", "dOffsetZJ",
    "dFXJ", "dFYJ", "dFZJ", "dMXJ", "dMYJ", "dMZJ",
]


def _format_value(raw: str) -> str:
    s = raw.strip()
    if s == "":
        return '""'
    try:
        f = float(s)
        if f == int(f) and "e" not in s.lower() and "." not in s and "E" not in s:
            return str(int(f))
        return repr(f)
    except ValueError:
        pass
    if s.startswith('"') and s.endswith('"'):
        return s
    if s.startswith("'") and s.endswith("'"):
        return f'"{s[1:-1]}"'
    escaped = s.replace('"', '\\"')
    return f'"{escaped}"'


def _render_inc_op_command(
    cmd: ParsedCommand,
    get_path: str,
    methods: dict[str, str],
) -> str:
    """OSIS: Cmd, name, op, group1, group2, ...
    op 不传给 include/remove，由 methods 映射方法名。
    """

    fields = cmd.fields[1:]
    if len(fields) < 2:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    name = _format_value(fields[0])
    op = fields[1].strip().lower()
    method = methods.get(op)
    if method is None:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    groups = ", ".join(_format_value(g) for g in fields[2:])
    if groups:
        return f"{get_path}({name}).{method}({groups})"
    return f"{get_path}({name}).{method}()"

def _load_prefix(lc_name: str) -> str:
    return f"engine.load.get({_format_value(lc_name)})"


def _format_girder_type(raw: str) -> str:
    """OSIS 导出 Steel/SteelBox → pyosis STEEL/STEELBOX。"""
    return _format_value(raw.strip().upper())


def _render_asgn_bd(cmd: ParsedCommand) -> str:
    """AsgnBd,bdNo,op,node1,... → assign(op, [node1, ...])，对齐 build.py。"""
    fields = cmd.fields[1:]
    if len(fields) < 2:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    bd_no = _format_value(fields[0])
    op = _format_value(fields[1])
    nodes = ", ".join(_format_value(v) for v in fields[2:])
    if nodes:
        return f"engine.boundary.get({bd_no}).assign({op}, [{nodes}])"
    return f"engine.boundary.get({bd_no}).assign({op}, [])"


def _render_rib(cmd: ParsedCommand) -> str:
    """Rib,secNo,type,name,... → add_rib_* 具体方法，避免 add_rib 分发器类型警告。"""
    fields = cmd.fields[1:]
    if len(fields) < 3:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    sec_no = _format_value(fields[0])
    rib_type = fields[1].strip()
    name = _format_value(fields[2])
    rest = [_format_value(v) for v in fields[3:]]
    prefix = f"engine.section.get({sec_no})"

    if rib_type == "Flat":
        return f"{prefix}.add_rib_flat({name}, {', '.join(rest)})"
    if rib_type == "T":
        return f"{prefix}.add_rib_t({name}, {', '.join(rest)})"
    if rib_type == "U":
        return f"{prefix}.add_rib_u({name}, {', '.join(rest)})"
    if rib_type in ("LL", "LR"):
        return f"{prefix}.add_rib_l({name}, {_format_value(rib_type)}, {', '.join(rest)})"

    raw = cmd.source.replace('"', '\\"')
    return f'engine.run("{raw}")'


def _render_steel_plate(cmd: ParsedCommand) -> str:
    """SteelPlate,secNo,girderType,... → girderType 转大写。"""
    fields = cmd.fields[1:]
    if len(fields) < 7:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    sec_no = _format_value(fields[0])
    girder = _format_girder_type(fields[1])
    rest = ", ".join(_format_value(v) for v in fields[2:])
    return f"engine.section.get({sec_no}).add_steel_plate({girder}, {rest})"


def _render_rib_layout(cmd: ParsedCommand, *, delete: bool = False) -> str:
    fields = cmd.fields[1:]
    if len(fields) < 4:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    sec_no = _format_value(fields[0])
    girder = _format_girder_type(fields[1])
    prefix = f"engine.section.get({sec_no})"
    if delete:
        plate = _format_value(fields[2])
        layout_no = _format_value(fields[3])
        return f"{prefix}.delete_rib_layout({girder}, {plate}, {layout_no})"
    rest = ", ".join(_format_value(v) for v in fields[2:])
    return f"{prefix}.add_rib_layout({girder}, {rest})"


def _render_rebar_l(cmd: ParsedCommand) -> str:
    """RebarL 分支，逻辑对齐 build.py generate_section。"""
    fields = cmd.fields[1:]
    if len(fields) < 4:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    sec_no = _format_value(fields[0])
    rebar_no = _format_value(fields[1])
    rebar_type = fields[2].strip().upper()
    mat_no = _format_value(fields[3])
    prefix = f"engine.section.get({sec_no})"

    if rebar_type == "POINT":
        if len(fields) < 7:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        y = _format_value(fields[4])
        z = _format_value(fields[5])
        dia = _format_value(fields[6])
        return f"{prefix}.add_rebar_point({rebar_no}, {mat_no}, {y}, {z}, {dia})"

    if rebar_type == "LINEA":
        if len(fields) < 12:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        y_ref = _format_value(fields[4])
        y_ref_val = _format_value(fields[5])
        z_ref = _format_value(fields[6])
        z_ref_val = _format_value(fields[7])
        num = _format_value(fields[8])
        interval = _format_value(fields[9])
        dia = _format_value(fields[10])
        return (
            f"{prefix}.add_rebar_line_a({rebar_no}, {mat_no}, {y_ref}, {y_ref_val}, "
            f"{z_ref}, {z_ref_val}, {num}, {interval}, {dia})"
        )

    if rebar_type == "LINEB":
        if len(fields) < 15:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        start_y = _format_value(fields[4])
        start_z = _format_value(fields[5])
        end_y = _format_value(fields[6])
        end_z = _format_value(fields[7])
        method = _format_value(fields[8])
        num = _format_value(fields[9])
        interval = _format_value(fields[10])
        layout_ref = _format_value(fields[11])
        has_end = _format_value(fields[12])
        dia = _format_value(fields[13])
        return (
            f"{prefix}.add_rebar_line_b({rebar_no}, {mat_no}, {start_y}, {start_z}, "
            f"{end_y}, {end_z}, {method}, {num}, {interval}, {layout_ref}, {has_end}, {dia})"
        )

    if rebar_type == "CIRCLE":
        if len(fields) < 12:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        center_y = _format_value(fields[4])
        center_z = _format_value(fields[5])
        radius = _format_value(fields[6])
        method = _format_value(fields[7])
        num = _format_value(fields[8])
        interval = _format_value(fields[9])
        diameter = _format_value(fields[10])
        return (
            f"{prefix}.add_rebar_circle({rebar_no}, {mat_no}, {center_y}, {center_z}, "
            f"{radius}, {method}, {num}, {interval}, {diameter})"
        )

    raw = cmd.source.replace('"', '\\"')
    return f'engine.run("{raw}")'


def _render_rebar_s(cmd: ParsedCommand) -> str:
    """RebarS 分支，逻辑对齐 build.py generate_section。"""
    fields = cmd.fields[1:]
    if len(fields) < 4:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    sec_no = _format_value(fields[0])
    rebar_type = fields[1].strip().upper()
    mat_no = _format_value(fields[2])
    prefix = f"engine.section.get({sec_no})"

    if rebar_type == "SHEARSTIRRUP":
        if len(fields) < 5:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        interval = _format_value(fields[3])
        area = _format_value(fields[4])
        return f"{prefix}.add_rebar_s_shear_stirrup({mat_no}, {interval}, {area})"

    if rebar_type == "BENTUPREBAR":
        if len(fields) < 5:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        interval = _format_value(fields[3])
        area = _format_value(fields[4])
        angle = _format_value(fields[5]) if len(fields) > 5 else "45"
        return f"{prefix}.add_rebar_s_bent_up({mat_no}, {interval}, {area}, {angle})"

    if rebar_type == "WEBVERTICALREBAR":
        if len(fields) < 8:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        interval = _format_value(fields[3])
        area = _format_value(fields[4])
        angle = _format_value(fields[5])
        effective_stress = _format_value(fields[6])
        reduction_factor = _format_value(fields[7])
        return (
            f"{prefix}.add_rebar_s_web_vertical({mat_no}, {interval}, {area}, "
            f"{angle}, {effective_stress}, {reduction_factor})"
        )

    if rebar_type == "TORSIONALSTIRRUP":
        if len(fields) < 6:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")'
        interval = _format_value(fields[3])
        longi_area = _format_value(fields[4])
        stirrup_area = _format_value(fields[5])
        return (
            f"{prefix}.add_rebar_s_torsional_stirrup({mat_no}, {interval}, "
            f"{longi_area}, {stirrup_area})"
        )

    raw = cmd.source.replace('"', '\\"')
    return f'engine.run("{raw}")'


def _render_load(
    cmd: ParsedCommand,
    current_lc: str | None,
) -> tuple[str, str | None]:
    """渲染 Load 命令，逻辑对齐 build.py generate_loadcase 分支。"""
    fields = cmd.fields[1:]
    if not fields:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")', current_lc

    # .out 特例: Load, entity, INITIAL, fxi, fyi, ...（无 lcName）
    if len(fields) >= 2 and fields[1].strip().upper() == "INITIAL":
        if current_lc is None:
            raw = cmd.source.replace('"', '\\"')
            return f'engine.run("{raw}")', current_lc
        entity = _format_value(fields[0])
        rest = ", ".join(_format_value(v) for v in fields[2:])
        p = _load_prefix(current_lc)
        if rest:
            return f"{p}.create_initial_force({entity}, {rest})", current_lc
        return f"{p}.create_initial_force({entity})", current_lc

    if len(fields) < 3:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")', current_lc

    load_type = fields[0].strip().upper()
    lc_name = fields[1]
    new_lc = lc_name
    p = _load_prefix(lc_name)
    a = fields[2:]

    if load_type == "GRAVITY":
        dX, dY, dZ = (_format_value(v) for v in a[:3])
        return f"{p}.create_gravity({dX}, {dY}, {dZ})", new_lc

    if load_type == "NFORCE":
        node, Fx, Fy, Fz, Mx, My, Mz = (_format_value(v) for v in a[:7])
        return f"{p}.create_nforce({node}, {Fx}, {Fy}, {Fz}, {Mx}, {My}, {Mz})", new_lc

    if load_type == "LINE":
        elem = _format_value(a[0])
        e_coord = _format_value(a[1])
        e_type = _format_value(a[2])
        i_params = a[3:12]
        j_params = a[12:21]
        params = [
            f"nEntity={elem}",
            f"eCoordSystem={e_coord}",
            f"eLoadType={e_type}",
        ]

        params += [f"{n}={_format_value(v)}" for n, v in zip(_LINE_I_NAMES, i_params)]
        params += [f"{n}={_format_value(v)}" for n, v in zip(_LINE_J_NAMES, j_params)]

        return f"{p}.create_line_load({', '.join(params)})", new_lc

    if load_type == "UTEMP":
        elem = _format_value(a[0])
        direct = _format_value(a[1])
        temp = _format_value(a[2])

        return f"{p}.create_uniform_temperature({elem}, direct={direct}, temp={temp})", new_lc


    if load_type == "GTEMP":
        elem = _format_value(a[0])
        direct = _format_value(a[1])
        gtype = _format_value(a[2])
        num = _format_value(a[3])
        rest = ", ".join(_format_value(v) for v in a[4:])

        if rest:
            return f"{p}.create_gradient_temperature({elem}, {direct}, {gtype}, {num}, {rest})", new_lc
        return f"{p}.create_gradient_temperature({elem}, {direct}, {gtype}, {num})", new_lc

    if load_type == "PST":
        shape = _format_value(a[0])
        tension_type = _format_value(a[1])
        force_type = _format_value(a[2])
        beg = _format_value(a[3])
        if len(a) > 4:
            end = _format_value(a[4])
            return (
                f"{p}.create_prestress({shape}, tension_type={tension_type}, "
                f"tension_force_type={force_type}, beg={beg}, end={end})",new_lc)

        if a[1].strip().upper() == "BEG":
            return (
                f"{p}.create_prestress({shape}, tension_type={tension_type}, "
                f"tension_force_type={force_type}, beg={beg}, end=None)",new_lc)

        if a[1].strip().upper() == "END":
            return (
                f"{p}.create_prestress({shape}, tension_type={tension_type}, "
                f"tension_force_type={force_type}, beg=None, end={beg})",new_lc)

        return (
            f"{p}.create_prestress({shape}, tension_type={tension_type}, "
            f"tension_force_type={force_type}, beg={beg}, end={beg})",new_lc)



    if load_type in ("PTF", "PTM"):
        elem = _format_value(a[0])
        e_coord = _format_value(a[1])
        is_moment = "True" if load_type == "PTM" else "False"
        offset_x = _format_value(a[3])
        offset_y = _format_value(a[4])
        offset_z = _format_value(a[5])
        fx = _format_value(a[6])
        fy = _format_value(a[7])
        fz = _format_value(a[8])
        return (f"{p}.create_concentrated_force({elem}, eCoordSystem={e_coord}, "
            f"is_moment={is_moment}, forces=[[{offset_x}, {offset_y}, {offset_z}, "
            f"{fx}, {fy}, {fz}]])",new_lc)

    if load_type == "DISPLACEMENT":
        entity = _format_value(a[0])
        rest = ", ".join(_format_value(v) for v in a[1:])
        if rest:
            return f"{p}.create_displacement({entity}, {rest})", new_lc
        return f"{p}.create_displacement({entity})", new_lc

    if load_type == "INITIAL":
        entity = _format_value(a[0])
        rest = ", ".join(_format_value(v) for v in a[1:])
        if rest:
            return f"{p}.create_initial_force({entity}, {rest})", new_lc
        return f"{p}.create_initial_force({entity})", new_lc


    if load_type == "CFORCE":
        entity = _format_value(a[0])
        load_kind = _format_value(a[1])
        force = _format_value(a[2])
        return f"{p}.create_cable_force({entity}, load_type={load_kind}, force={force})", new_lc



    rest = ", ".join(_format_value(v) for v in a)

    raw = cmd.source.replace('"', '\\"')

    return f'engine.run("{raw}")', new_lc


def _render_live_grade(cmd: ParsedCommand) -> str:
    """渲染 LiveGrade，对齐 build.py 与各 create_* 签名。"""
    fields = cmd.fields[1:]
    if len(fields) < 3:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    name = _format_value(fields[0])
    code = _format_value(fields[1])
    load_type = fields[2].strip().upper()
    lt = _format_value(fields[2])
    p = "engine.live.grade"

    if load_type in ("HIGHWAY_I", "HIGHWAY_II"):
        return f"{p}.create_highway({name}, code={code}, live_load_type={lt})"

    if load_type == "VEHICLE":
        return f"{p}.create_vehicle({name}, code={code}, live_load_type={lt})"

    if load_type == "CROWD":
        bridge_type = _format_value(fields[3]) if len(fields) > 3 else '"BRIDGE_COMMON"'
        para = _format_value(fields[4]) if len(fields) > 4 else "10.0"
        return (
            f"{p}.create_crowd({name}, code={code}, live_load_type={lt}, "
            f"bridge_type={bridge_type}, para={para})"
        )

    if load_type.startswith("FATIGUE"):
        if load_type == "FATIGUE_II" and len(fields) > 3:
            para = _format_value(fields[3])
            return f"{p}.create_fatigue({name}, code={code}, live_load_type={lt}, para={para})"
        return f"{p}.create_fatigue({name}, code={code}, live_load_type={lt})"

    if load_type == "VG":
        grp_num = _format_value(fields[3]) if len(fields) > 3 else "1"
        pairs = fields[4:]
        layout_items = [
            f"({_format_value(pairs[i])}, {_format_value(pairs[i + 1])})"
            for i in range(0, len(pairs) - len(pairs) % 2, 2)
        ]
        layout = f"[{', '.join(layout_items)}]" if layout_items else "[]"
        return (
            f"{p}.create_custom({name}, code={code}, live_load_type={lt}, "
            f"grp_num={grp_num}, veh_grp_layout={layout})"
        )

    raw = cmd.source.replace('"', '\\"')
    return f'engine.run("{raw}")'


_MU_PARAM_COUNTS = {
    "SIMPLE": 4,
    "CONTINUOUS": 5,
    "ARCH": 5,
    "CABLE_STAYED": 2,
    "CABLE_STAYED_AUX": 2,
    "SUSPENSION": 5,
    "BRIDGE_TYPE_CUSTOM": 1,
    "CUSTOM": 1,
}


def _live_case_prefix(raw_name: str, current_live_case: str | None) -> str:
    """对齐 build.py _get_live_prefix。"""
    if current_live_case is not None and raw_name == current_live_case:
        return "lc."
    return f"engine.live.case.get({_format_value(raw_name)})."


def _render_infl_algo(cmd: ParsedCommand) -> str:
    """渲染 InflAlgo，逻辑对齐 build.py generate_analysis。"""
    fields = cmd.fields[1:]
    if len(fields) < 3:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    name = _format_value(fields[0])
    algo_type = fields[1].strip().upper()
    p = "engine.live.lane"

    if algo_type == "VE":
        length = _format_value(fields[2])
        wheel = _format_value(fields[3])
        ori = _format_value(fields[4])
        ref = fields[5].strip()
        esel = _format_value(fields[6])
        if ref == "0":
            offset_y = _format_value(fields[7]) if len(fields) > 7 else "0.0"
            offset_z = _format_value(fields[8]) if len(fields) > 8 else "0.0"
            return (
                f"{p}.create_ve({name}, length={length}, wheel={wheel}, "
                f"orientation={ori}, ref=0, ref_elems={esel}, "
                f"offset_y={offset_y}, offset_z={offset_z})"
            )
        spline = _format_value(fields[7]) if len(fields) > 7 else '""'
        return (
            f"{p}.create_ve({name}, length={length}, wheel={wheel}, "
            f"orientation={ori}, ref=1, spline_name={spline})"
        )

    if algo_type == "TCB":
        crossbeam = _format_value(fields[2])
        length = _format_value(fields[3])
        wheel = _format_value(fields[4])
        ori = _format_value(fields[5])
        ref = fields[6].strip()
        if ref == "0":
            ref_elems = _format_value(fields[7]) if len(fields) > 7 else '""'
            offset_y = _format_value(fields[8]) if len(fields) > 8 else "0.0"
            offset_z = _format_value(fields[9]) if len(fields) > 9 else "0.0"
            return (
                f"{p}.create_tcb({name}, crossbeam_elems={crossbeam}, length={length}, "
                f"wheel={wheel}, orientation={ori}, ref=0, ref_elems={ref_elems}, "
                f"offset_y={offset_y}, offset_z={offset_z})"
            )
        spline = _format_value(fields[7]) if len(fields) > 7 else '""'
        return (
            f"{p}.create_tcb({name}, crossbeam_elems={crossbeam}, length={length}, "
            f"wheel={wheel}, orientation={ori}, ref=1, spline_name={spline})"
        )

    raw = cmd.source.replace('"', '\\"')
    return f'engine.run("{raw}")'


def _render_live_anal(cmd: ParsedCommand) -> tuple[str, str | None]:
    """渲染 LiveAnal，返回 (代码行, 当前活载工况名)。"""
    fields = cmd.fields[1:]
    if len(fields) < 3:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")', None
    raw_name = fields[0]
    name = _format_value(raw_name)
    code = _format_value(fields[1])
    sub_cmb = _format_value(fields[2])
    return f"lc = engine.live.case.create({name}, code={code}, sub_cmb_type={sub_cmb})", raw_name


def _render_live_anal_factor(cmd: ParsedCommand, current_live_case: str | None) -> str:
    fields = cmd.fields[1:]
    if len(fields) < 2:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    raw_name = fields[0]
    prefix = _live_case_prefix(raw_name, current_live_case)
    factors = ", ".join(_format_value(v) for v in fields[1:])
    return f"{prefix}set_trans_reduction_factors({factors})"


def _render_live_anal_opt(cmd: ParsedCommand, current_live_case: str | None) -> str:
    fields = cmd.fields[1:]
    if len(fields) < 4:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    raw_name = fields[0]
    prefix = _live_case_prefix(raw_name, current_live_case)
    sub_name = _format_value(fields[1])
    min_lanes = _format_value(fields[2])
    max_lanes = _format_value(fields[3])
    return f"{prefix}set_lane_count({sub_name}, {min_lanes}, {max_lanes})"


def _render_live_anal_inc(cmd: ParsedCommand, current_live_case: str | None) -> str:
    """渲染 LiveAnalInc (op=a/m)，逻辑对齐 build.py。"""
    fields = cmd.fields[1:]
    if len(fields) < 3:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    raw_name = fields[0]
    op = fields[1].strip()
    if op not in ("a", "m"):
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    if len(fields) < 7:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    sub_name = _format_value(fields[2])
    grade_name = _format_value(fields[3])
    scalar = _format_value(fields[4])
    calc_mu = fields[5].strip() == "1"
    extra = fields[7:]
    func_name = "create_sub" if op == "a" else "modify_sub"
    prefix = _live_case_prefix(raw_name, current_live_case)
    params = f"{sub_name}, {grade_name}, scalar={scalar}, calc_mu={calc_mu}"

    if calc_mu:
        bridge_type = _format_value(fields[6])
        n_mu = _MU_PARAM_COUNTS.get(fields[6].strip(), 0)
        mu_params = extra[:n_mu] if n_mu else []
        lane_names = extra[n_mu:]
        params += f", bridge_type={bridge_type}"
        if mu_params:
            mu_str = ", ".join(_format_value(p) for p in mu_params)
            params += f", mu_params=[{mu_str}]"
    else:
        lane_names = extra

    if lane_names:
        lane_str = ", ".join(_format_value(l) for l in lane_names)
        params += f", lane_names=[{lane_str}]"

    return f"{prefix}{func_name}({params})"


def _render_live_anal_del(cmd: ParsedCommand) -> str:
    fields = cmd.fields[1:]
    if not fields:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    return f"engine.live.case.delete({_format_value(fields[0])})"


def _render_live_anal_mod(cmd: ParsedCommand) -> str:
    fields = cmd.fields[1:]
    if len(fields) < 2:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'
    return (
        f"engine.live.case.rename({_format_value(fields[0])}, "
        f"{_format_value(fields[1])})"
    )

def _route_key(name: str) -> str:
    return _ROUTE_ALIASES.get(name.lower(), name)

def _render_command(cmd: ParsedCommand) -> str:
    route = ROUTES.get(_route_key(cmd.name))

    if route is None:
        raw = cmd.source.replace('"', '\\"')
        return f'engine.run("{raw}")'

    if _route_key(cmd.name) == "LiveGrade":
        return _render_live_grade(cmd)

    if _route_key(cmd.name) == "InflAlgo":
        return _render_infl_algo(cmd)

    if _route_key(cmd.name) == "LiveAnalDel":
        return _render_live_anal_del(cmd)

    if _route_key(cmd.name) == "LiveAnalMod":
        return _render_live_anal_mod(cmd)

    key = _route_key(cmd.name)
    if key == "AsgnBd":
        return _render_asgn_bd(cmd)
    if key == "Rib":
        return _render_rib(cmd)
    if key == "SteelPlate":
        return _render_steel_plate(cmd)
    if key == "RibLayout":
        return _render_rib_layout(cmd)
    if key == "RibLayoutDel":
        return _render_rib_layout(cmd, delete=True)
    if key == "RebarL":
        return _render_rebar_l(cmd)
    if key == "RebarS":
        return _render_rebar_s(cmd)

    # SetlAnalInc：跳过 op，与 build.py args[3:] 一致
    if key == "SetlAnalInc":
        return _render_inc_op_command(
            cmd,
            "engine.settlement.get",
            {"a": "include", "r": "remove"},
        )

    fields = cmd.fields[1:]

    if isinstance(route, tuple) and route[0] == "chain":
        _, get_path, method_name, skip = route[:4]
        rest_prefix = route[4] if len(route) > 4 else 0
        if len(fields) <= skip:
            return f"{get_path}().{method_name}()"
        key = fields[skip]
        rest_fields = list(fields[:rest_prefix]) + list(fields[skip + 1:])
        formatted_key = _format_value(key)
        formatted_rest = [_format_value(v) for v in rest_fields]
        return f"{get_path}({formatted_key}).{method_name}({', '.join(formatted_rest)})"

    method = route
    formatted = [_format_value(v) for v in fields]
    return f"{method}({', '.join(formatted)})"


def generate_lines(commands: List[ParsedCommand]) -> List[str]:
    """生成 Python 调用行；矩阵命令合并为 engine.matrix(...)。"""

    lines: List[str] = []

    accumulator = MatrixAccumulator()

    current_lc_name: str | None = None
    current_live_case: str | None = None

    for cmd in commands:
        # 处理矩阵维度命令
        if cmd.kind == "matrix_dim":
            flushed = accumulator.flush()
            if flushed:
                lines.append(flushed)
            accumulator.on_dim(cmd.fields)
            continue

        # 处理矩阵赋值命令
        if cmd.kind == "matrix_assign":
            accumulator.on_assign(cmd.matrix_name, cmd.matrix_indices, cmd.matrix_value)
            continue

        # 刷新矩阵累加器
        flushed = accumulator.flush()
        if flushed:
            lines.append(flushed)

        # 处理活载工况命令
        if _route_key(cmd.name) == "LoadCase" and len(cmd.fields) >= 2:
            current_lc_name = cmd.fields[1]

        # 处理其他命令
        key = _route_key(cmd.name)
        if key == "Load":
            line, current_lc_name = _render_load(cmd, current_lc_name)
        elif key == "LiveAnal":
            line, new_live = _render_live_anal(cmd)
            if new_live is not None:
                current_live_case = new_live
        # 处理活载工况因子命令
        elif key == "LiveAnalFactor":
            line = _render_live_anal_factor(cmd, current_live_case)
        # 处理活载工况选项命令
        elif key == "LiveAnalOpt":
            line = _render_live_anal_opt(cmd, current_live_case)
        # 处理活载工况增加命令
        elif key == "LiveAnalInc":
            line = _render_live_anal_inc(cmd, current_live_case)
        # 处理其他命令
        else:
            line = _render_command(cmd)

        lines.append(line)

    # 刷新矩阵累加器
    flushed = accumulator.flush()

    if flushed:
        lines.append(flushed)

    # 返回生成后的代码行
    return lines

def generate(commands: List[ParsedCommand]) -> str:
    return "\n".join(generate_lines(commands)) + "\n"