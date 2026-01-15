import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.linalg import solve
import json
import debugpy

# # 启用调试器，监听端口 5678
# debugpy.listen(5678)
# print("等待调试器连接...")
# debugpy.wait_for_client()  # 这行会阻塞，直到调试器连接
# print("调试器已连接，开始执行...")

# 导入OSIS功能
from pyosis.control import *
from pyosis.general import *
from pyosis.section import *
from pyosis.material import *
from pyosis.node import *
from pyosis.element import *
from pyosis.boundary import *
from pyosis.load import *
from pyosis.post import *

def dict_to_json_txt(data, filename):
    """将字典以JSON格式写入文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"字典已写入文件: {filename}")

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def log_to_file(message='', filename='result.txt'):
    fp = open(filename, 'a', encoding='utf-8')
    fp.write(message)
    fp.close()

log_to_file("\n======start======\n")
# -------------------------- 1. 基本参数定义 --------------------------
# 材料参数
E = 200e3  # 弹性模量(MPa)
sigma_allow = 300  # 强度设计值(MPa)
# 截面参数（编号0-4对应5种截面）
sections = {
    0: {'D': 219, 't': 12, 'A': 7803.7, 'I': 4.19e7},
    1: {'D': 180, 't': 8, 'A': 4322.8, 'I': 1.602e7},
    2: {'D': 114, 't': 5, 'A': 1712.2, 'I': 2.55e6},
    3: {'D': 89, 't': 4, 'A': 1068.1, 'I': 9.668e5},
    4: {'D': 45, 't': 3, 'A': 395.8, 'I': 8.773e4},
        5: {'D': 10, 't': 1, 'A': 10, 'I': 1E2}
}
for idx in sections:
    A = sections[idx]['A']
    I = sections[idx]['I']
    sections[idx]['i'] = np.sqrt(I / A)  # 回转半径(mm)

# 边界与荷载条件（固定铰支座：(0,5)和(15,5)）
fixed_nodes = np.array([[0, 5], [15, 5]])  # 固定节点（x,y单位：m）
load_nodes = np.array([[7.5, 0], [20, 0]])  # 荷载作用节点
loads = np.array([[0, -1000], [200, 0]])    # 荷载（Fx,Fy单位：kN）

# 优化参数设置
n_var_nodes = 0# 可变节点数量（可调整）
var_node_bounds = [[7.5, 20], [0, 5]]  # 可变节点坐标范围（x:0-20m，y:0-5m）
pop_size = 10    # 遗传算法种群规模
n_generations = 3  # 迭代次数
crossover_prob = 0.8  # 交叉概率
mutation_prob = 0.2  # 变异概率

# -------------------------- 2. 桁架结构计算核心函数 --------------------------
def create_truss(var_nodes):
    """创建桁架结构：合并固定节点、荷载节点和可变节点，生成杆件连接（二元体规则）"""
    # 明确包含固定节点、荷载节点、可变节点，确保荷载节点存在
    all_nodes = np.vstack([fixed_nodes, load_nodes, var_nodes])  # 所有节点（N×2矩阵）
    n_nodes = len(all_nodes)
    edges = []  # 杆件连接（节点索引对）
    
    # 基础连接：荷载节点之间、固定节点与荷载/可变节点、荷载节点与可变节点
    # 固定节点之间连接
    edges.append((2, 3))  # 两个荷载点连接
    # 固定节点与荷载节点连接
    edges.append((0, 2))
    for i in range(2, 2+len(load_nodes)):
        # edges.append((0, i))
        edges.append((1, i))
    # 固定节点/荷载节点与可变节点连接
    var_node_start_idx = 2 + len(load_nodes)
    for i in range(var_node_start_idx, n_nodes):
        # 连接到所有固定节点
        edges.append((0, i))
        edges.append((1, i))
        # 连接到所有荷载节点
        for j in range(2, var_node_start_idx):
            edges.append((j, i))
        # 可变节点之间相互连接（保证几何不变）
        for j in range(var_node_start_idx, i):
            edges.append((j, i))
    
    # 去重并转换为数组
    edges = list(set(edges))
    edges = np.array([sorted(edge) for edge in edges])
    return all_nodes, edges

###############################################################
# 需要设置成OSIS计算
###############################################################
def calculate_internal_forces(nodes, edges, loads, load_node_ids, section_ids):
    # 固定设置
    osis_clear()

    osis_acel(9.8066)
    osis_calc_tendon(1)
    osis_calc_con_force(1)
    osis_calc_shrink(1)
    osis_calc_creep(1)
    osis_calc_shear(1)
    osis_calc_rlx(1)
    osis_mod_loc_coor(0)
    osis_inc_tendon(1)
    osis_nl(0, 0)
    osis_ln_srch(0)
    osis_auto_ts(0)
    osis_mod_opt(0)

    osis_section(1, "圆形截面1", "Circle", {"CircleType": "Hollow", "D": 0.219,"Tw": 0.012})
    osis_section(2, "圆形截面2", "Circle", {"CircleType": "Hollow", "D": 0.180,"Tw": 0.008})
    osis_section(3, "圆形截面3", "Circle", {"CircleType": "Hollow", "D": 0.114,"Tw": 0.005})
    osis_section(4, "圆形截面4", "Circle", {"CircleType": "Hollow", "D": 0.089,"Tw": 0.004})
    osis_section(5, "圆形截面5", "Circle", {"CircleType": "Hollow", "D": 0.045,"Tw": 0.003})

    osis_material(1, "钢材1", "STEEL", "JTGD64_2015", "Q345", -1, 0.05)

    # 需要调整的
    for i in range(len(nodes)):
        n = nodes[i]
        osis_node(i + 1, n[0], n[1], 0)

    for i in range(len(edges)):
        e = edges[i]
        osis_element(i + 1, "BEAM3D", {"nNode1": e[0] + 1, "nNode2": e[1] + 1, "nMat": 1, "nSec1": section_ids[i] + 1, "nSec2": section_ids[i] + 1, 
          "nYTrans": 1, "nZTrans": 1, "dStrain": 0.00, "bFlag": 0, "dTheta": 0.00, "bWarping": 0})

    osis_boundary(1, "GENERAL", {"nCoor": -1, "bDX": 1, "bDY": 1, "bDZ": 1, "bRX": 1, "bRY": 1, "bRZ": 1, "bRW": 1})
    osis_assign_boundary(1, "a", [1, 2])

    osis_loadcase("自定义工况1", "USER", 1, "两个力")
    for i in range(len(loads)):
        l = loads[i]        # 力的大小  单位 kN
        idx = load_node_ids[i]  # 节点ID
        osis_load("NFORCE", "自定义工况1", {"nNO": idx + 1, "dFX": l[0] * 1000, "dFY": l[1] * 1000, "dFZ": 0, "dMX": 0, "dMY": 0, "dMZ": 0})

    osis_solve()
    isok, error, ef = osis_elem_force("自定义工况1", "EF", "BEAM3D")
    dict_to_json_txt(ef, "liu_output.json")   # 保存结果用于调试
    # log_to_file(f"ef = {ef}\n")
    ef_fx = ef["Fx"]      # 轴向内力
    # log_to_file(f"ef_fx = {ef_fx}\n")
    N = np.array(ef_fx, dtype=float) / 1000  # 换算成kN
    # log_to_file(f"N = {N}\n")
    return N

def calculate_volume(nodes, edges, section_ids):
    """计算结构总体积（mm³）"""
    volume = 0
    for e, (i, j) in enumerate(edges):
        L = np.sqrt((nodes[j,0]-nodes[i,0])**2 + (nodes[j,1]-nodes[i,1])**2) * 1000  # mm
        A = sections[section_ids[e]]['A']
        volume += A * L
    return volume / 1e9  # 转换为m³

def check_constraints(nodes, edges, section_ids, N):
    """检查约束条件：强度约束+稳定约束"""
    n_edges = len(edges)
    feasible = True
    sigma_list = []
    stability_list = []
    
    for e in range(n_edges):
        A = sections[section_ids[e]]['A']
        N_e = N[e]
        L = np.sqrt((nodes[edges[e][1],0]-nodes[edges[e][0],0])**2 + 
                    (nodes[edges[e][1],1]-nodes[edges[e][0],1])**2) * 1000  # mm
        
        # 强度约束
        sigma = abs(N_e * 1000) / A  # 转换为MPa（N_e:kN→N）
        sigma_list.append(sigma)
        if sigma > sigma_allow:
            feasible = False
        
        # 稳定约束（受压杆件）
        if N_e < 0:
            i = sections[section_ids[e]]['i']
            lambda_val = L / i  # 长细比
            sigma_cr = (np.pi**2 * E) / (lambda_val**2)  # 欧拉临界应力
            stability_list.append(sigma_cr)
            if abs(sigma) > sigma_cr:
                feasible = False
    
    return feasible, sigma_list, stability_list

# -------------------------- 3. 遗传算法优化 --------------------------
def initialize_population():
    """初始化种群：每个个体包含可变节点坐标和杆件截面编号"""
    population = []
    for _ in range(pop_size):
        # 随机生成可变节点坐标（n_var_nodes×2）
        var_nodes = np.random.uniform(
            low=[var_node_bounds[0][0], var_node_bounds[1][0]],
            high=[var_node_bounds[0][1], var_node_bounds[1][1]],
            size=(n_var_nodes, 2)
        )
        # 生成杆件截面编号（0-4）
        nodes, edges = create_truss(var_nodes)
        section_ids = np.random.randint(0, 5, size=len(edges))
        population.append((var_nodes, section_ids))
    return population

def fitness(individual):
    """适应度函数：可行解返回体积，不可行解返回惩罚值"""
    var_nodes, section_ids = individual
    nodes, edges = create_truss(var_nodes)
    
    # 找到荷载作用节点的索引（容忍浮点数误差）
    load_node_ids = []
    for load_node in load_nodes:
        # 匹配时允许1e-6的误差，避免浮点数精度问题
        match_idx = np.where(np.isclose(nodes, load_node, atol=1e-6).all(axis=1))[0]
        if len(match_idx) == 0:
            return 10  # 惩罚值：未找到荷载节点
        idx = match_idx[0]
        load_node_ids.append(idx)
    
    # 计算内力
    try:
        N = calculate_internal_forces(nodes, edges, loads, load_node_ids, section_ids)
    except:
        return 10  # 计算失败返回惩罚值
    
    # 检查约束
    feasible, sigma_list, stability_list = check_constraints(nodes, edges, section_ids, N)
    
    if feasible:
        volume = calculate_volume(nodes, edges, section_ids)
        return volume
    else:
        # 惩罚：不可行解返回较大值
        return 10

def selection(population, fitnesses):
    """选择操作：轮盘赌选择（最小化问题，适应度取倒数）"""
    # 避免除以0，给极小值加保护
    fitnesses = [f if f > 1e-6 else 1e-6 for f in fitnesses]
    total_fitness = sum(1/f for f in fitnesses)
    probabilities = [1/(f*total_fitness) for f in fitnesses]
    # 确保概率和为1（浮点误差修正）
    probabilities = np.array(probabilities) / np.sum(probabilities)
    selected = np.random.choice(len(population), size=pop_size, p=probabilities)
    new_population = [population[i] for i in selected]
    return new_population

def crossover(parent1, parent2):
    """交叉操作：节点坐标算术交叉，截面编号单点交叉"""
    var_nodes1, sec1 = parent1
    var_nodes2, sec2 = parent2
    
    # 节点坐标交叉
    alpha = np.random.rand()
    var_nodes_child = alpha * var_nodes1 + (1 - alpha) * var_nodes2
    
    # 截面编号交叉（处理长度不同的情况）
    len1, len2 = len(sec1), len(sec2)
    if len1 == len2 and len1 > 1:
        cross_point = np.random.randint(1, len1)
        sec_child = np.hstack([sec1[:cross_point], sec2[cross_point:]])
    else:
        # 长度不同时，取较长的为基础，短的补到末尾
        if len1 > len2:
            sec_child = sec1.copy()
            sec_child[:len2] = sec2
        else:
            sec_child = sec2.copy()
            sec_child[:len1] = sec1
    
    return (var_nodes_child, sec_child)

def mutate(individual):
    """变异操作：节点坐标随机扰动，截面编号随机替换"""
    var_nodes, sec = individual
    
    # 节点坐标变异（带边界约束）
    mutation_step = 0.5  # 扰动步长（m）
    for i in range(len(var_nodes)):
        if np.random.rand() < mutation_prob:
            var_nodes[i] += np.random.uniform(-mutation_step, mutation_step, size=2)
            # 边界裁剪
            var_nodes[i, 0] = np.clip(var_nodes[i, 0], var_node_bounds[0][0], var_node_bounds[0][1])
            var_nodes[i, 1] = np.clip(var_nodes[i, 1], var_node_bounds[1][0], var_node_bounds[1][1])
    
    # 截面编号变异
    for i in range(len(sec)):
        if np.random.rand() < mutation_prob:
            sec[i] = np.random.randint(0, 5)
    
    return (var_nodes, sec)

def genetic_algorithm():
    """遗传算法主流程"""
    population = initialize_population()
    best_fitness = float('inf')
    best_individual = None
    
    for gen in range(n_generations):
        # 计算适应度
        fitnesses = [fitness(ind) for ind in population]
        
        # 更新最优解
        current_best_idx = np.argmin(fitnesses)
        current_best_fitness = fitnesses[current_best_idx]
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[current_best_idx]
        
        # 输出迭代信息
        if (gen + 1) % 10 == 0:
            print(f"第{gen+1}代，最优体积：{best_fitness:.4f} m³")

        log_to_file(f"第{gen+1}代，最优体积：{best_fitness:.4f} m³\n")
        
        # 选择、交叉、变异
        new_population = selection(population, fitnesses)
        offspring = []
        for i in range(0, pop_size, 2):
            parent1 = new_population[i]
            parent2 = new_population[i+1] if i+1 < pop_size else new_population[i]
            if np.random.rand() < crossover_prob:
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
                offspring.append(mutate(child1))
                offspring.append(mutate(child2))
            else:
                offspring.append(mutate(parent1))
                offspring.append(mutate(parent2))
        
        population = offspring[:pop_size]
    
    return best_individual, best_fitness

# -------------------------- 4. 结果分析与可视化 --------------------------
def analyze_result(best_individual):
    """分析最优解：计算内力、约束满足情况"""
    var_nodes, section_ids = best_individual
    nodes, edges = create_truss(var_nodes)
    
    # 找到荷载作用节点索引
    load_node_ids = []
    for load_node in load_nodes:
        match_idx = np.where(np.isclose(nodes, load_node, atol=1e-6).all(axis=1))[0][0]
        load_node_ids.append(match_idx)
    
    # 计算内力
    N = calculate_internal_forces(nodes, edges, loads, load_node_ids, section_ids)
    
    # 检查约束
    feasible, sigma_list, stability_list = check_constraints(nodes, edges, section_ids, N)
    
    # 计算体积
    volume = calculate_volume(nodes, edges, section_ids)
    
    # 输出结果
    
    log_to_file("=== 最优桁架结构结果 ===\n")
    log_to_file(f"结构总体积：{volume:.4f} m³\n")
    log_to_file(f"约束满足情况：{'可行' if feasible else '不可行'}\n")
    log_to_file("\n杆件信息（索引-节点对-截面编号-内力(kN)-应力(MPa)）：\n")
    print("=== 最优桁架结构结果 ===\n")
    print(f"结构总体积：{volume:.4f} m³")
    print(f"约束满足情况：{'可行' if feasible else '不可行'}")
    print("\n杆件信息（索引-节点对-截面编号-内力(kN)-应力(MPa)）：")
    for e, (i, j) in enumerate(edges):
        sigma = sigma_list[e] if e < len(sigma_list) else 0
        print(f"{e:2d} - ({i:2d},{j:2d}) - {section_ids[e]:1d} - {N[e]:6.1f} - {sigma:5.1f}")
        log_to_file(f"{e:2d} - ({i:2d},{j:2d}) - {section_ids[e]:1d} - {N[e]:6.1f} - {sigma:5.1f}\n")
        
    
    return nodes, edges, N, section_ids, volume


def plot_truss(nodes, edges, section_ids, N):
    """
    绘制桁架结构：
    - 节点：区分固定/荷载/可变，带编号
    - 杆件：区分拉/压，带编号+截面编号，粗细对应截面大小
    - 荷载：统一箭头长度，标注荷载值（kN）
    """
    plt.figure(figsize=(14, 7))
    G = nx.Graph()
    
    # 1. 添加节点和杆件
    for i, (x, y) in enumerate(nodes):
        G.add_node(i, pos=(x, y))
    for e, (i, j) in enumerate(edges):
        G.add_edge(i, j, section=section_ids[e], force=N[e], idx=e)
    
    # 2. 节点相关配置
    pos = nx.get_node_attributes(G, 'pos')
    # 分类节点索引
    fixed_node_ids = [np.where(np.isclose(nodes, fn, atol=1e-6).all(axis=1))[0][0] for fn in fixed_nodes]
    load_node_ids = [np.where(np.isclose(nodes, ln, atol=1e-6).all(axis=1))[0][0] for ln in load_nodes]
    var_node_ids = [i for i in range(len(nodes)) if i not in fixed_node_ids + load_node_ids]
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, nodelist=fixed_node_ids, node_color='red', node_size=300, label='固定铰支座')
    nx.draw_networkx_nodes(G, pos, nodelist=load_node_ids, node_color='orange', node_size=200, label='荷载作用节点')
    nx.draw_networkx_nodes(G, pos, nodelist=var_node_ids, node_color='blue', node_size=150, label='可变节点')
    # 节点编号（白色加粗，偏移避免遮挡）
    pos_node_label = {i: (x, y) for i, (x, y) in pos.items()}
    node_labels = {i: str(i) for i in range(len(nodes))}
    nx.draw_networkx_labels(G, pos_node_label, labels=node_labels, font_size=9, font_color='white', font_weight='bold')

    # 3. 杆件相关配置
    max_A = max([sections[s]['A'] for s in section_ids])
    edge_labels = {}  # 杆件标注：编号+截面
    for e, (i, j) in enumerate(edges):
        # 杆件基础属性
        A = sections[section_ids[e]]['A']
        width = 3 * (A / max_A)  # 归一化粗细（放大系数3，更易区分）
        color = 'red' if N[e] > 0 else 'blue'  # 拉力红，压力蓝
        # 绘制杆件
        nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], width=width, edge_color=color, alpha=0.8)
        # 杆件标注：格式 "杆件号-截面号"（如"0-1"）
        edge_labels[(i, j)] = f"{e}-{section_ids[e]}"
    
    # 绘制杆件编号+截面（居中显示，黑色字体）
    pos_edge_label = nx.spring_layout(G, pos=pos, fixed=pos.keys(), k=0.1)  # 标注位置微调
    nx.draw_networkx_edge_labels(G, pos_edge_label, edge_labels=edge_labels, 
                                 font_size=8, font_color='black', label_pos=0.5)

    # 4. 荷载标注（统一箭头长度，显示荷载值）
    load_scale = 0.001  # 荷载箭头长度缩放系数（统一长度）
    for idx, (x, y) in enumerate(load_nodes):
        fx, fy = loads[idx]
        # 统一箭头长度：按荷载矢量模长归一化
        load_mag = np.sqrt(fx**2 + fy**2)
        if load_mag == 0:
            continue
        fx_norm = fx / load_mag * load_scale * 20  # 统一长度（20为基准）
        fy_norm = fy / load_mag * load_scale * 20
        # 绘制荷载箭头
        plt.arrow(x, y, fx_norm, fy_norm, head_width=0.25, head_length=0.25, 
                  fc='black', ec='black', alpha=0.9)
        # 标注荷载值（格式：Fx,Fy (kN)）
        load_text = f"({fx:.0f},{fy:.0f})kN"
        # 文字位置：箭头末端偏移
        text_x = x + fx_norm + (0.3 if fx_norm > 0 else -0.8)
        text_y = y + fy_norm + (0.3 if fy_norm > 0 else -0.8)
        plt.text(text_x, text_y, load_text, fontsize=9, fontweight='bold', 
                 bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))

    # 5. 图表全局设置
    plt.xlabel('x坐标 (m)', fontsize=10)
    plt.ylabel('y坐标 (m)', fontsize=10)
    plt.title('优化后的桁架结构布置图（节点/杆件编号+截面+荷载值）', fontsize=12, fontweight='bold')
    # 自定义图例（补充杆件含义）
    from matplotlib.lines import Line2D
    custom_lines = [
        Line2D([0], [0], color='red', lw=4, label='受拉杆件'),
        Line2D([0], [0], color='blue', lw=4, label='受压杆件'),
        Line2D([0], [0], color='black', lw=1, marker='>', markersize=10, label='荷载（统一长度）')
    ]
    plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + custom_lines, 
               loc='upper right', fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()  # 自适应布局，避免标注遮挡
    plt.savefig('result_fig.png')
    # plt.show()

# -------------------------- 5. 主程序运行 --------------------------
if __name__ == "__main__":
    # 运行遗传算法优化
    print("开始桁架结构优化...")
    best_ind, best_vol = genetic_algorithm()
    
    # 分析结果
    nodes, edges, N, section_ids, volume = analyze_result(best_ind)
    
    # 可视化
    plot_truss(nodes, edges, section_ids, N)
