from rb_atom import RbAtom
import rb_atom_config as C

if __name__ == '__main__':
    atom = RbAtom(C.Rb87)
    B = 0.2  # (Tesla)
    E_levels = atom.energy_levels(B)
