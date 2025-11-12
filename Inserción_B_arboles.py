# Implementa aquí todos los procesos necesarios para la operación de inserción. 
# Pueden modificar la extensión del documento para que se ajuste al lenguaje de su elección y comentar estas instrucciones.

# Clase para representar un nodo de un B-árbol
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t                   # Grado mínimo (mínimo número de claves)
        self.leaf = leaf             # Indica si es hoja
        self.keys = []               # Lista de claves
        self.children = []           # Lista de hijos

    def insert_non_full(self, key):
        """Inserta una clave en un nodo que no está lleno"""
        i = len(self.keys) - 1

        # Caso 1: nodo hoja
        if self.leaf:
            # Encontrar la posición correcta de la nueva clave
            while i >= 0 and key < self.keys[i]:
                i -= 1
            self.keys.insert(i + 1, key)
        else:
            # Buscar el hijo apropiado
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1

            # Si el hijo está lleno, dividirlo antes de insertar
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        """Divide un hijo lleno en dos nodos"""
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)

        # Claves para el nuevo nodo z
        z.keys = y.keys[t:]
        mid_key = y.keys[t - 1]
        y.keys = y.keys[:t - 1]

        # Si no es hoja, dividir también los hijos
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        # Insertar el nuevo hijo y clave mediana en el nodo actual
        self.children.insert(i + 1, z)
        self.keys.insert(i, mid_key)


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        """Inserta una nueva clave en el B-Tree"""
        root = self.root

        # Si la raíz está llena, dividirla
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(root)
            new_root.split_child(0)
            i = 0
            if key > new_root.keys[0]:
                i += 1
            new_root.children[i].insert_non_full(key)
            self.root = new_root
        else:
            root.insert_non_full(key)

    def search(self, key, node=None):
        """Búsqueda en el B-Tree"""
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.leaf:
            return False

        return self.search(key, node.children[i])

    def print_tree(self, node=None, level=0):
        """Imprime el B-Tree por niveles"""
        if node is None:
            node = self.root
        print("Nivel", level, ":", node.keys)
        if not node.leaf:
            for child in node.children:
                self.print_tree(child, level + 1)
              
# Ejemplo de uso:
if __name__ == "__main__":
    btree = BTree(t=2)  # Grado mínimo = 2

    datos = [10, 20, 5, 6, 12, 30, 7, 17]
    for d in datos:
        btree.insert(d)

    btree.print_tree()

'''
Se crea un B-Árbol desde cero, el resultado se vería:
         [10, 20]
        /    |     \
   [5,6,7] [12,17] [30]
'''
