# Implementa aquí la operación de búsqueda. 
# Pueden modificar la extensión del documento para que se ajuste al lenguaje de su elección y comentar estas instrucciones.

# Clase para representar un nodo de un B-árbol
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t                # Grado mínimo
        self.leaf = leaf          # Indica si es hoja
        self.keys = []            # Claves del nodo
        self.children = []        # Hijos del nodo

# Clase para representar el B-árbol completo
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, leaf=True)
        self.t = t

    # FUNCIÓN DE BÚSQUEDA
    def search(self, k, x=None):
        # Busca una clave 'k' en el B-árbol. Si la encuentra, devuelve el nodo y la posición de la clave. 
        # Si no, devuelve None.
        if x is None:
            x = self.root

        # Buscar la primera clave mayor o igual a k
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1

        # Si la clave está en este nodo
        if i < len(x.keys) and x.keys[i] == k:
            print(f"=> BIEN :) Clave {k} encontrada en el nodo con claves: {x.keys}")
            return (x, i)

        # Si el nodo es hoja, la clave no está
        if x.leaf:
            print(f"=> MAL :( Clave {k} NO encontrada (nodo hoja {x.keys})")
            return None

        # Si no es hoja, buscar en el hijo correspondiente
        print(f"\nBuscando clave {k} en el subárbol del hijo {i} con claves {x.keys}")
        return self.search(k, x.children[i])

    # INSERCIÓN (para crear ejemplo)
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_non_full(new_root, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t - 1):
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(t, leaf=y.leaf)
        x.keys.insert(i, y.keys[t - 1])
        x.children.insert(i + 1, z)
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:t - 1]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    # Mostrar el árbol (visualización)
    def show(self, x=None, level=0):
        if x is None:
            x = self.root
        print("Nivel", level, "Claves:", x.keys)
        if not x.leaf:
            for child in x.children:
                self.show(child, level + 1)


# EJEMPLO DE LA BÚSQUEDA

# Creamos un B-árbol de grado 2 (Mismo B-Árbol de todos las implementaciones)
btree = BTree(2)

for k in [10, 20, 5, 6, 12, 30, 7, 17]:
    btree.insert(k)

print("Estructura actual del B-árbol:")
btree.show()

# Buscamos varias claves
print("\nResultados de la búsqueda:")
btree.search(6)    # Clave que sí existe
btree.search(15)   # Clave que no existe
btree.search(17)   # Clave que sí existe

'''
Se construye un B-árbol de grado 2 e insertan las claves [10, 20, 5, 6, 12, 30, 7, 17].
            [10, 20]
           /    |     \
    [5,6,7]  [12,17]  [30]

La búsqueda comienza en la raíz:
  - Si la clave está ahí → éxito :)
  - Si no, sigue al hijo correspondiente según el rango de valores.
  - Si llega a una hoja sin encontrarla → la clave no está :(

En el ejemplo:
- Buscando clave 6
  - Buscando clave 6 en el subárbol del hijo 0 con claves [10, 20]
  - Clave 6 encontrada en el nodo con claves: [5, 6, 7]

- Buscando clave 15
  - Buscando clave 15 en el subárbol del hijo 1 con claves [10, 20]
  - Clave 15 NO encontrada (nodo hoja [12, 17])

- Buscando clave 17
  - Buscando clave 17 en el subárbol del hijo 1 con claves [10, 20]
  - Clave 17 encontrada en el nodo con claves: [12, 17]
