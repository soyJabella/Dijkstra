import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QLineEdit,QSpinBox, QDialog,QWidget
import math
import networkx as nx  # Importación del paquete NetworkX, paquete para graficar
import matplotlib.pyplot as plt  # Importación del paquete Matplotlib

def agregar_arista(G, u, v, w=1, di=True):
    G.add_edge(u, v, weight=w)
 
    # Si el grafo no es dirigido
    if not di:
        # Agrego otra arista en sentido contrario
        G.add_edge(v, u, weight=w)
 
class Vertice:
  """Clase que define los vértices de los gráficas"""
  def __init__(self, i):
    """Método que inicializa el vértice con sus atributos
    id = identificador
    vecinos = lista de los vértices con los que está conectado por una arista
    visitado = flag para saber si fue visitado o no
    padre = vértice visitado un paso antes
    costo = valor que tiene recorrerlo"""
    self.id = i
    self.vecinos = []
    self.visitado = False
    self.padre = None
    self.costo = float('inf')
 
  def agregarVecino(self, v, p):
    """Método que agrega los vertices que se encuentre conectados por una arista a la lista de vecinos 
    de un vertice, revisando si éste aún no se encuentra en la lista de vecinos"""
    if v not in self.vecinos:
      self.vecinos.append([v, p])
 
class Grafica_dijkstra:
  
  """Clase que define los vértices de las gráficas"""
  def __init__(self):
    """vertices = diccionario con los vertices de la grafica"""
    self.vertices = {}
   
 
  def agregarVertice_dijkstra(self, id):
    """Método que agrega vértices, recibiendo el índice y la heuristica (para A* puede que no se reciba) revisando si éste no existe en el diccionario
    de vértices"""
    if id not in self.vertices:
      self.vertices[id] = Vertice(id)
 
  def agregarArista_dijkstra(self, a, b, p):
    """Método que agrega aristas, recibiendo el índice de dos vertices y revisando si existen estos en la lista
    de vertices, además de recibir el peso de la arista , el cual se asigna a ambos vértices por medio del método
    agregar vecino"""
    if a in self.vertices and b in self.vertices:
      self.vertices[a].agregarVecino(b, p)
      self.vertices[b].agregarVecino(a, p)
 
  
  def camino(self, a, b):
    """Método que va guardando en la lista llamada 'camino' los nodos en el orden que sean visitados y actualizando dicha
    lista con los vértices con el menor costo"""
    camino = []
    actual = b
    while actual != None:
      camino.insert(0, actual)
      actual = self.vertices[actual].padre
    return [camino, self.vertices[b].costo]
 
  def minimo(self, l):
    """Método que recibe la lista de los vertices no visitados, revisa si su longitud es mayor a cero(indica que 
    aún hay vértices sin visitar), y realiza comparaciones de los costos de cada vértice en ésta lista para encontrar
    el de menor costo"""
    if len(l) > 0:
      m = self.vertices[l[0]].costo
      v = l[0]
      for e in l:
        if m > self.vertices[e].costo:
          m = self.vertices[e].costo
          v = e
      return v
    return None
  
  def dijkstra(self, a):
    """Método que sigue el algortimo de Dijkstra
    1. Asignar a cada nodo una distancia tentativa: 0 para el nodo inicial e infinito para todos los nodos restantes. Predecesor nulo para todos.
    2. Establecer al nodo inicial como nodo actual y crear un conjunto de nodos no visitados.
    3. Para el nodo actual, considerar a todos sus vecinos no visitados con peso w.
      a) Si la distancia del nodo actual sumada al peso w es menor que la distancia tentativa actual de ese vecino,
      sobreescribir la distancia con la suma obtenida y guardar al nodo actual como predecesor del vecino
    4. Cuando se termina de revisar a todos los vecino del nodo actual, se marca como visitado y se elimina del conjunto no  visitado
    5. Continúa la ejecución hasta vaciar al conjunto no visitado
    6. Seleccionar el nodo no visitado con menor distancia tentativa y marcarlo como el nuevo nodo actual. Regresar al punto 3
    """
    if a in self.vertices:
      # 1 y 2
      self.vertices[a].costo = 0
      actual = a
      noVisitados = []
      
      for v in self.vertices:
        if v != a:
          self.vertices[v].costo = float('inf')
        self.vertices[v].padre = None
        noVisitados.append(v)
 
      while len(noVisitados) > 0:
        #3
        for vec in self.vertices[actual].vecinos:
          if self.vertices[vec[0]].visitado == False:
            # 3.a
            if self.vertices[actual].costo + vec[1] < self.vertices[vec[0]].costo:
              self.vertices[vec[0]].costo = self.vertices[actual].costo + vec[1]
              self.vertices[vec[0]].padre = actual
 
        # 4
        self.vertices[actual].visitado = True
        noVisitados.remove(actual)
 
        # 5 y 6
        actual = self.minimo(noVisitados)
    else:
      return False
 
class inicio (QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/andre/OneDrive/Escritorio/Basura_Monica/Inicio.ui",self)
        self.matriz = []
        self.GenerarN.clicked.connect(self.generarMatriz)
        self.Generar.clicked.connect(self.generarGrafo)
        
    def generarMatriz(self):
        num = self.NumNodos.value()
        self.matriz = [[0 for i in range(num)] for j in range(num)]
        for i in range(num):
            for j in range(num):
                self.matriz[i][j] = QSpinBox()
    
        self.setVisible(False)
        for i in range(num):
            for j in range(num):
                self.gridLayout.addWidget(self.matriz[i][j], *(i,j))
        self.setVisible(True)
    
    def generarGrafo(self):
        gui=Grafo( self)
        self.setVisible(False)
        gui.show()    
        

class Grafo(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("C:/Users/andre/OneDrive/Escritorio/Basura_Monica/Grafo.ui",self)
        self.num = parent.NumNodos.value()
        self.matriz = [[0 for i in range(self.num)] for j in range(self.num)]
        
        for i in range(self.num):
            for j in range(self.num):
                self.matriz[i][j] = parent.matriz[i][j].value()
                
        self.g = Grafica_dijkstra()
        
        for i in range(self.num):
            self.g.agregarVertice_dijkstra(i)
        
        for i in range(self.num):
            for j in range(self.num):
                if(self.matriz[i][j]!=0):
                    self.g.agregarArista_dijkstra(i,j,self.matriz[i][j])
        
        self.buscar.clicked.connect(self.buscarRutaCorta)
    
    def buscarRutaCorta(self):
        nOrigen = self.nodoOrigen.value()
        nDestino = self.nodoDestino.value()
        self.g.dijkstra(nOrigen)
        self.consola.setText("La ruta más rápida por Dijkstra junto con su costo es:\n" + str(self.g.camino(nOrigen, nDestino)))
        
        G = nx.DiGraph()
        
        for i in range(self.num):
            for j in range(self.num):
                if(self.matriz[i][j]!=self.matriz[j][i]):
                    agregar_arista(G, str(i), str(j), self.matriz[i][j])
                else:
                    agregar_arista(G, str(i), str(j), self.matriz[i][j], False)
        pos = nx.layout.planar_layout(G)  
        nx.draw_networkx(G, pos)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Representación del Grafo")
        self.frame = plt
        plt.show()
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    gui=inicio()
    gui.show()
    sys.exit(app.exec_())