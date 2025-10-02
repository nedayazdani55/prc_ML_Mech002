# truss_fea.py
import numpy as np

def assemble_truss(nodes, elements):
    N = len(nodes)
    K = np.zeros((2*N, 2*N))
    for el in elements:
        i, j = el['n1'], el['n2']
        xi, yi = nodes[i]
        xj, yj = nodes[j]
        dx = xj - xi; dy = yj - yi
        L = np.hypot(dx, dy)
        if L == 0:
            raise ValueError("Zero length element")
        c = dx / L; s = dy / L
        AE_L = el['A'] * el['E'] / L
        k = AE_L * np.array([
            [ c*c,  c*s, -c*c, -c*s],
            [ c*s,  s*s, -c*s, -s*s],
            [-c*c, -c*s,  c*c,  c*s],
            [-c*s, -s*s,  c*s,  s*s]
        ])
        dofs = [2*i, 2*i+1, 2*j, 2*j+1]
        for a in range(4):
            for b in range(4):
                K[dofs[a], dofs[b]] += k[a,b]
    return K

def solve_truss(nodes, elements, loads, fixed_dofs):
    """
    nodes: list of [x,y]
    elements: list of dicts with keys n1,n2,A,E
    loads: global force vector length 2N
    fixed_dofs: list of DOF indices fixed (0-based)
    returns: dict {u, elem_forces, elem_stresses, max_stress, max_disp}
    """
    N = len(nodes)
    K = assemble_truss(nodes, elements)
    F = np.array(loads, dtype=float).reshape(-1)
    all_dofs = np.arange(2*N)
    free = np.setdiff1d(all_dofs, fixed_dofs)
    Kff = K[np.ix_(free, free)]
    Ff = F[free]
    # Solve (can raise LinAlgError on singular)
    uf = np.linalg.solve(Kff, Ff)
    u = np.zeros(2*N, dtype=float)
    u[free] = uf

    elem_forces = []
    elem_stresses = []
    for el in elements:
        i, j = el['n1'], el['n2']
        xi, yi = nodes[i]; xj, yj = nodes[j]
        L = np.hypot(xj - xi, yj - yi)
        c = (xj - xi) / L; s = (yj - yi) / L
        dofs = [2*i, 2*i+1, 2*j, 2*j+1]
        ue = u[dofs]
        # axial extension = (u_j - u_i) · direction
        ext = (ue[2] - ue[0]) * c + (ue[3] - ue[1]) * s
        axial = el['E'] * el['A'] / L * ext
        stress = axial / el['A']
        elem_forces.append(float(axial))
        elem_stresses.append(float(stress))
    max_stress = float(max(np.abs(elem_stresses))) if elem_stresses else 0.0
    max_disp = float(np.max(np.abs(u))) if u.size else 0.0
    return {
        "u": u.tolist(),
        "elem_forces": elem_forces,
        "elem_stresses": elem_stresses,
        "max_stress": max_stress,
        "max_disp": max_disp
    }

# Demo builder for a simple parametric truss (used by API)
def build_demo_truss(load=-1000.0, A=1e-4, E=210e9):
    nodes = [[0.0,0.0],[1.0,0.0],[2.0,0.0],[1.0,1.0]]
    elements = [
        {'n1':0,'n2':1,'A':A,'E':E},
        {'n1':1,'n2':2,'A':A,'E':E},
        {'n1':0,'n2':3,'A':A,'E':E},
        {'n1':1,'n2':3,'A':A,'E':E},
        {'n1':2,'n2':3,'A':A,'E':E},
    ]
    F = [0.0]*(2*len(nodes))
    # apply vertical load at node index 2 (third node) -> DOF 5
    F[5] = load
    fixed = [0,1,6]  # fix node0 both DOFs and node3 x DOF
    return nodes, elements, F, fixed

if __name__ == "__main__":
    # quick local test
    nodes,elements,F,fixed = build_demo_truss(load=-1000.0)
    out = solve_truss(nodes,elements,F,fixed)
    print("max stress (Pa):", out["max_stress"])
    print("max disp (m):", out["max_disp"])




















# # truss_fea.py
# import numpy as np

# def assemble_truss(nodes, elements):
#     """
#     nodes: array Nx2
#     elements: list of dicts [{'n1':i,'n2':j,'A':area,'E':E}, ...] indices: 0-based
#     returns K (2N x 2N)
#     """
#     N = len(nodes)
#     K = np.zeros((2*N,2*N))
#     for el in elements:
#         i, j = el['n1'], el['n2']
#         xi, yi = nodes[i]
#         xj, yj = nodes[j]
#         dx = xj - xi; dy = yj - yi
#         L = np.hypot(dx, dy)
#         c = dx / L; s = dy / L
#         AE_L = el['A'] * el['E'] / L
#         k = AE_L * np.array([
#             [ c*c,  c*s, -c*c, -c*s],
#             [ c*s,  s*s, -c*s, -s*s],
#             [-c*c, -c*s,  c*c,  c*s],
#             [-c*s, -s*s,  c*s,  s*s]
#         ])
#         dofs = [2*i, 2*i+1, 2*j, 2*j+1]
#         for a in range(4):
#             for b in range(4):
#                 K[dofs[a], dofs[b]] += k[a,b]
#     return K

# def solve_truss(nodes, elements, loads, fixed_dofs):
#     """
#     loads: global force vector length 2N
#     fixed_dofs: list of DOF indices fixed
#     returns displacement vector u, element_forces list, stresses list
#     """
#     N = len(nodes)
#     K = assemble_truss(nodes, elements)
#     F = np.array(loads).reshape(-1)
#     all_dofs = np.arange(2*N)
#     free = np.setdiff1d(all_dofs, fixed_dofs)
#     Kff = K[np.ix_(free, free)]
#     Ff = F[free]
#     uf = np.linalg.solve(Kff, Ff)
#     u = np.zeros(2*N)
#     u[free] = uf

#     elem_forces = []
#     elem_stresses = []
#     for el in elements:
#         i, j = el['n1'], el['n2']
#         xi, yi = nodes[i]; xj, yj = nodes[j]
#         L = np.hypot(xj - xi, yj - yi)
#         c = (xj - xi) / L; s = (yj - yi) / L
#         dofs = [2*i, 2*i+1, 2*j, 2*j+1]
#         ue = u[dofs]
#         ext = (-c)*ue[0] + (-s)*ue[1] + c*ue[2] + s*ue[3]  # axial extension
#         axial = el['E'] * el['A'] / L * ext
#         stress = axial / el['A']
#         elem_forces.append(axial)
#         elem_stresses.append(stress)
#     return u, elem_forces, elem_stresses

# # Example usage:
# if __name__ == "__main__":
#     # sample 4-node truss
#     nodes = np.array([[0.0,0.0],[1.0,0.0],[2.0,0.0],[1.0,1.0]])
#     # elements: connect nodes (0-based indexing)
#     E = 210e9; A = 1e-4
#     elements = [
#         {'n1':0,'n2':1,'A':A,'E':E},
#         {'n1':1,'n2':2,'A':A,'E':E},
#         {'n1':0,'n2':3,'A':A,'E':E},
#         {'n1':1,'n2':3,'A':A,'E':E},
#         {'n1':2,'n2':3,'A':A,'E':E},
#     ]
#     # global loads (2*4 = 8 DOFs)
#     F = np.zeros(8); F[5] = -1000.0  # apply vertical load at node 2 (index 2 -> DOF 5)
#     fixed = [0,1,6]  # fix node0 both DOFs and node3 x DOF as example
#     u, forces, stresses = solve_truss(nodes, elements, F, fixed)
#     print("displacements:", u.reshape(-1,2))
#     print("max stress (Pa):", max(np.abs(stresses)))
