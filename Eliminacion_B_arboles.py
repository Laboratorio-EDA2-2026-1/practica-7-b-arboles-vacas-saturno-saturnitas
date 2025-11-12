# Implementa aquí todos los procesos necesarios para la operación de eliminación. 
# Pueden modificar la extensión del documento para que se ajuste al lenguaje de su elección y comentar estas instrucciones.
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    # INSERCIÓN
    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            self.keys.insert(i + 1, key)
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)

        z.keys = y.keys[t:]
        mid = y.keys[t - 1]
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        self.children.insert(i + 1, z)
        self.keys.insert(i, mid)

    # ELIMINACIÓN
    def remove(self, key):
        # Elimina una clave del subárbol con raíz en este nodo
        t = self.t
        i = self.find_key(key)

        # Caso 1: la clave está en este nodo
        if i < len(self.keys) and self.keys[i] == key:
            if self.leaf:
                # Caso 1a: es hoja entonces se elimina directamente
                self.keys.pop(i)
            else:
                # Caso 1b: es nodo interno
                self.remove_internal_node(i)
        else:
            # Caso 2: la clave no está en este nodo
            if self.leaf:
                # No se encontró
                print(f"La clave {key} no existe en el árbol.")
                return
            flag = (i == len(self.keys))
            if len(self.children[i].keys) < t:
                self.fill(i)
            if flag and i > len(self.keys):
                self.children[i - 1].remove(key)
            else:
                self.children[i].remove(key)

    def remove_internal_node(self, i):
        """Elimina una clave de un nodo interno"""
        key = self.keys[i]
        if len(self.children[i].keys) >= self.t:
            pred = self.get_predecessor(i)
            self.keys[i] = pred
            self.children[i].remove(pred)
        elif len(self.children[i + 1].keys) >= self.t:
            succ = self.get_successor(i)
            self.keys[i] = succ
            self.children[i + 1].remove(succ)
        else:
            self.merge(i)
            self.children[i].remove(key)

    def get_predecessor(self, i):
        current = self.children[i]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def get_successor(self, i):
        current = self.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def fill(self, i):
        # Garantiza que el hijo tenga al menos t-1 claves antes de seguir
        if i != 0 and len(self.children[i - 1].keys) >= self.t:
            self.borrow_from_prev(i)
        elif i != len(self.keys) and len(self.children[i + 1].keys) >= self.t:
            self.borrow_from_next(i)
        else:
            if i != len(self.keys):
                self.merge(i)
            else:
                self.merge(i - 1)

    def borrow_from_prev(self, i):
        child = self.children[i]
        sibling = self.children[i - 1]
        child.keys.insert(0, self.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        self.keys[i - 1] = sibling.keys.pop()

    def borrow_from_next(self, i):
        child = self.children[i]
        sibling = self.children[i + 1]
        child.keys.append(self.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        self.keys[i] = sibling.keys.pop(0)

    def merge(self, i):
        child = self.children[i]
        sibling = self.children[i + 1]
        child.keys.append(self.keys[i])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        self.keys.pop(i)
        self.children.pop(i + 1)

    def find_key(self, key):
        # Encuentra el índice de la primera clave >= key
        for i, k in enumerate(self.keys):
            if k >= key:
                return i
        return len(self.keys)

    # UTILIDADES
    def traverse(self):
        """Recorre e imprime el árbol en orden"""
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].traverse()
            print(self.keys[i], end=" ")
        if not self.leaf:
            self.children[len(self.keys)].traverse()

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        root = self.root
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

    def remove(self, key):
        if not self.root:
            print("El árbol está vacío.")
            return

        self.root.remove(key)

        # Si la raíz quedó vacía, se ajusta
        if len(self.root.keys) == 0:
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if node is None:
            print("(árbol vacío)")
            return
        print("Nivel", level, ":", node.keys)
        if not node.leaf:
            for child in node.children:
                self.print_tree(child, level + 1)

# Ejemplo:
if __name__ == "__main__":
    btree = BTree(t=2)

    datos = [10, 20, 5, 6, 12, 30, 7, 17]
    for d in datos:
        btree.insert(d)

    print("Árbol inicial:")
    btree.print_tree()

    # Eliminaciones de prueba
    print("\nEliminando 6...")
    btree.remove(6)
    btree.print_tree()

    print("\nEliminando 13 (no existe)...")
    btree.remove(13)

    print("\nEliminando 7 y 17...")
    btree.remove(7)
    btree.remove(17)
    btree.print_tree()

    print("\nEliminando 20...")
    btree.remove(20)
    btree.print_tree()


'''
Partimos del árbol resultante de la inserción:
            [10, 20]
           /    |     \
   [5,6,7]   [12,17]   [30]

Paso 1: Eliminar 6
La clave 6 está en el hijo izquierdo [5,6,7], que es una hoja.
En este caso, la eliminación es directa, simplemente se quita el valor del nodo.
            [10, 20]
           /    |     \
      [5,7]   [12,17]   [30]

Paso 2: Eliminar 13
uscamos la clave 13.
No está en la raíz [10,20].
Tampoco está en el subárbol central [12,17].
No existe en el árbol, así que no se hace ningún cambio.
            [10, 20]
           /    |     \
      [5,7]   [12,17]   [30]

Paso 3: Eliminar 7
La clave 7 está en [5,7], que es una hoja.
Se elimina directamente.

Ahora ese nodo queda con solo una clave [5], pero como aún tiene al menos t−1 = 1 clave, no hay problema.
            [10, 20]
           /    |     \
        [5]   [12,17]   [30]

Paso 4: Eliminar 17
La clave 17 está en el nodo [12,17], que también es hoja.
Así que se elimina directamente.

El nodo queda con una sola clave [12], que ya vimos que no hay problema.
            [10, 20]
           /    |     \
        [5]    [12]    [30]

Paso 5: Eliminar 20
La clave 20 está en la raíz, que no es hoja, así que aplicamos la regla:

Si el hijo derecho ([30]) tiene al menos t = 2 claves, tomamos su sucesor;
si no, tomamos el predecesor o fusionamos.

Aquí, [30] tiene solo una clave, así que no podemos tomar prestado.
Lo mismo con el hijo central [12].

Por lo tanto, fusionamos el hijo central y derecho junto con la clave 20.
           [10]
          /    \
       [5]   [12,30]
'''
