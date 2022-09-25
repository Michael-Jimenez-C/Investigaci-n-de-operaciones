{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "private_outputs": true,
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyNeDRSO3yO0treAkLAJAwoh",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Michael-Jimenez-C/Investigaci-n-de-operaciones/blob/main/Tarea2IO/Metodo-Grafico-Terminado.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import matplotlib.pyplot as plt\n",
        "from matplotlib.colors import ListedColormap\n",
        "import numpy as np"
      ],
      "metadata": {
        "id": "Zp1r5KiRqBXT"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Funcion"
      ],
      "metadata": {
        "id": "09ZBNMMkwnud"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "class Condicion:\n",
        "  MENOR_IGUAL=0\n",
        "  MAYOR_IGUAL=1\n",
        "  MENOR=2\n",
        "  MAYOR=3\n",
        "  def __init__(self,coeficiente:float,corte:float, tipo:int=MENOR, en='y'):\n",
        "    '''\n",
        "    Crea una condicion de la forma y (<=)(>=)(<)(>) coeficiente*x+corte\n",
        "    En caso de que el atributo \"en='x'\" se va a ignorar el coeficiente y\n",
        "    determinará una expresion de la forma x (<=)(>=)(<)(>) corte.\n",
        "\n",
        "    '''\n",
        "    self.coeficiente=coeficiente\n",
        "    self.corte=corte\n",
        "    self.tipo=tipo\n",
        "    self.en=en\n",
        "    self.funcion=None\n",
        "\n",
        "  def __add__(self,other):\n",
        "    '''\n",
        "    Estas operaciones no se supone deban usarse por el usuario, son solo para poder hacer calculos sobre las intersecciones entre dos funciones.\n",
        "    '''\n",
        "    return Condicion(self.coeficiente+other.coeficiente,self.corte+other.corte,self.tipo)\n",
        "\n",
        "  def __sub__(self,other):\n",
        "    '''\n",
        "    Estas operaciones no se supone deban usarse por el usuario, son solo para poder hacer calculos sobre las intersecciones entre dos funciones.\n",
        "    '''\n",
        "    return Condicion(self.coeficiente-other.coeficiente,self.corte-other.corte,self.tipo)\n",
        "\n",
        "  def __repr__(self):\n",
        "    #Muestra la funcion\n",
        "    if self.en=='y':\n",
        "      return \"y {} {}x+({})\".format([\"<=\",\">=\",\"<\",\">\"][self.tipo],self.coeficiente,self.corte)\n",
        "    return \"x {} ({})\".format([\"<=\",\">=\",\"<\",\">\"][self.tipo],self.corte)\n",
        "\n",
        "  def condicion(valor:float, tipo:int, en:str):\n",
        "    '''\n",
        "    Es un método que permite hacer una condicion simple por ejemplo y<3 o x>=5\n",
        "    '''\n",
        "    return Condicion(0,valor,tipo,en)\n",
        "\n",
        "  def getCorte(self):\n",
        "    #Retorna los puntos de corte con el eje horizontal y el eje vertical\n",
        "    return ((0,self.corte),((-self.corte)/self.coeficiente,0))\n",
        "\n",
        "  def __evaluar(self,x):\n",
        "    #Evalua un valor como si fuera una igualdad\n",
        "    if self.en=='x':\n",
        "      return np.nan\n",
        "        \n",
        "    if self.funcion==None:\n",
        "      self.funcion=lambda x:self.coeficiente*x+self.corte\n",
        "    return self.funcion(x)\n",
        "\n",
        "  \n",
        "  def evaluar(self,x):\n",
        "    #Evalua un valor como si fuera una igualdad\n",
        "    if self.en=='x':\n",
        "      return np.array(2*[self.corte]), np.array([-10,10])\n",
        "        \n",
        "    if self.funcion==None:\n",
        "      self.funcion=lambda x:self.coeficiente*x+self.corte\n",
        "    return x,self.funcion(x)\n",
        "\n",
        "  def evaluarCondicion(self,x,y=0):\n",
        "    #evalua si se cumple la condicion para un numero dado, redondeado a 5 decimales.\n",
        "    f=[lambda a,b: a<=b,lambda a,b: a>=b][self.tipo%2]\n",
        "    if self.en=='y':\n",
        "      return f(round(y,5),round(self.__evaluar(x),5))\n",
        "    else:\n",
        "      return f(x,self.corte)\n",
        "\n",
        "  def getInterseccion(self, other):\n",
        "    #Calcula la interseccion de dos rectas\n",
        "    if ((self.en=='x' or other.en=='x') and not(self.en=='x' and other.en=='x')):\n",
        "      a,b=(self,other) if self.en=='x' else (other,self)\n",
        "      return a.corte, b.__evaluar(a.corte)\n",
        "    if (self.en=='y' and other.en=='y'):\n",
        "      p=(self-other).getCorte()[1][0]\n",
        "      return p,self.__evaluar(p)\n",
        "    return None\n"
      ],
      "metadata": {
        "id": "iTtgdNW3q1h0"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Solver"
      ],
      "metadata": {
        "id": "ikUs3VZYwhJ3"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "class Solver:\n",
        "  def __init__(self, condiciones):\n",
        "    '''\n",
        "    Solver se encargará de hallar los vertices y de optimizar la funcion objetivo,\n",
        "    sin embargo no se va a pedir la funcion objetivo en el constructor\n",
        "    '''\n",
        "    self.condiciones=condiciones\n",
        "  def __puntos(self):\n",
        "    #retorna todas las intersecciones, pues se quiere poder utilizarlas para optimizar la funcion objetivo\n",
        "    k=self.condiciones\n",
        "    p=[]\n",
        "    for i in range(len(k)):\n",
        "      for j in range(i+1,len(k)):\n",
        "        try:\n",
        "          p.append(k[i].getInterseccion(k[j]))\n",
        "        except:\n",
        "          pass\n",
        "    return p\n",
        "\n",
        "  def vertices(self):\n",
        "    p=self.__puntos()\n",
        "    s=p[:]\n",
        "    for i in self.condiciones:\n",
        "      for j in p:\n",
        "        if (not i.evaluarCondicion(j[0],j[1])):\n",
        "          if j in s:\n",
        "            s.remove(j)\n",
        "    return s\n",
        "  \n",
        "  def optimizar(self,funcionObjetivo=lambda x,y: x+y, modo='max'):\n",
        "    puntos=self.vertices()\n",
        "    valores=[]\n",
        "    for i in puntos:\n",
        "      valores.append(funcionObjetivo(i[0],i[1]))\n",
        "    valores=np.array(valores)\n",
        "    if modo=='max':\n",
        "      return puntos[np.argmax(valores)], valores.max()\n",
        "    else:\n",
        "      return puntos[np.argmax(-valores)], valores.min()\n",
        "    \n"
      ],
      "metadata": {
        "id": "VQxuJ-MrwtNu"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Clase Graficador"
      ],
      "metadata": {
        "id": "rPGeSBywvTMb"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "class Graficador:\n",
        "  def __init__(self,condiciones,solver,xlims,ylims):\n",
        "    self.condiciones=condiciones\n",
        "    self.xlims=xlims\n",
        "    self.ylims=ylims\n",
        "    self.solver=solver\n",
        "  def plot(self):\n",
        "    condiciones,xlims,ylims,solver=self.condiciones,self.xlims,self.ylims,self.solver\n",
        "    X__=[np.linspace(xlims[0],xlims[1],300),np.linspace(ylims[0],ylims[1],300)]\n",
        "    Y__=None\n",
        "    for i in condiciones:\n",
        "      temp=np.array([[i.evaluarCondicion(x0,x1) for x0 in X__[0]] for x1 in X__[1]],dtype=\"int64\")\n",
        "      if type(Y__)==type(None):\n",
        "        Y__=-temp\n",
        "        continue\n",
        "      Y__-=temp\n",
        "    cmap = ListedColormap([\"white\",\"cyan\"])\n",
        "    plt.figure(figsize=(7,7))\n",
        "    plt.pcolormesh(X__[0],X__[1],-np.minimum(Y__.min()+1,Y__),cmap=cmap)\n",
        "    plt.xlim(xlims[0],xlims[1])\n",
        "    plt.ylim(ylims[0],ylims[1])\n",
        "\n",
        "    x=X__[0]\n",
        "    for i in condiciones:\n",
        "      try:\n",
        "        plt.plot(x,i.evaluar(x))\n",
        "      except:\n",
        "        pass\n",
        "\n",
        "    y=np.array(solver.vertices()).T\n",
        "    if len(y)>0:\n",
        "      plt.scatter(y[0],y[1],color=\"red\")\n",
        "    plt.grid()\n",
        "    for i in condiciones:\n",
        "        xi,yi=i.evaluar(x)\n",
        "        plt.plot(xi,yi)\n",
        "    plt.show()"
      ],
      "metadata": {
        "id": "RvSTgzXphQL-"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Final"
      ],
      "metadata": {
        "id": "iuGkHUEd05In"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "class MetodoGrafico:\n",
        "  def visualizacion(condiciones, xlims, ylims):\n",
        "    solver=Solver(condiciones)\n",
        "    graf=Graficador(condiciones,solver,xlims,ylims).plot()\n",
        "  \n",
        "  def optimizar(condiciones,funcionObjetivo,modo):\n",
        "    solver=Solver(condiciones)\n",
        "    return solver.optimizar(funcionObjetivo,modo)"
      ],
      "metadata": {
        "id": "X-KT-og3xGiz"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "MetodoGrafico.visualizacion(condiciones,(0,3),(0,3))\n",
        "print(MetodoGrafico.optimizar(condiciones,lambda x,y: 2*x +y,'max'))"
      ],
      "metadata": {
        "id": "eXLMgo2L12TL"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}