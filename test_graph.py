import pandas as pd
import numpy as np

# Configurar seed para reprodutibilidade
np.random.seed(42)

# Criar dados de teste
n_points = 10  # Reduzido para 10 pontos

# Criar x valores de 0 a 100
x = np.linspace(0, 100, n_points)

# Criar três séries diferentes
y1 = np.random.uniform(0, 100, n_points)  # Valores aleatórios entre 0 e 100
y2 = x + np.random.normal(0, 10, n_points)  # Tendência linear com ruído
y3 = 50 + 30 * np.sin(x * np.pi / 50)  # Onda senoidal entre 20 e 80

# Criar DataFrame
df = pd.DataFrame({
    'X': x,
    'Série A': y1,
    'Série B': y2,
    'Série C': y3
})

# Arredondar valores para 2 casas decimais
df = df.round(2)

# Salvar para CSV
df.to_csv('test_data.csv', index=False)

# Executar a aplicação
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from Gráficos import GraphApp
    
    app = QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_()) 