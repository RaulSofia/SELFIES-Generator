from csv import DictReader
import ast
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.rdCoordGen import AddCoords

def my_eval(str):
    testes = [
        (int),
        (float)
    ]
    for teste in testes:
        try:
            return teste(str)
        except ValueError:
            continue
    return str

def get_configs(file_path):
    with open(file_path, 'r', encoding='utf-8')as file:
        reader = DictReader(file)
        configs = list(reader)[0]
        for config in configs:
            configs[config] = my_eval(configs[config])
    return configs

def remove_isotopes(smile):
    mol = Chem.MolFromSmiles(smile)
    mol_block = Chem.MolToMolBlock(mol)
    new_mol_block = []
    for line in mol_block.split('\n'):
        if 'M  ISO' not in line:
            new_mol_block += [line]
    new_mol_block = '\n'.join(new_mol_block)
    new_mol = Chem.MolFromMolBlock(new_mol_block)
    new_smile = Chem.MolToSmiles(new_mol)
    return(new_smile)

if __name__ == "__main__":
    smile = r"Cn1c(=O)c2c(nc(/C=C/c3cccc(Cl)c3)n2[11CH3])n(C)c1=O"
    new_smile = remove_isotopes(smile)
    mol = Chem.MolFromSmiles(smile)
    new_mol = Chem.MolFromSmiles(new_smile)
    AddCoords(mol)
    AddCoords(new_mol)
    img = Draw.MolsToGridImage(mols=[mol, new_mol], legends=['original', 'no isotopes'])
    img.show()
