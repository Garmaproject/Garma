import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import logging
import re
from utils import get_table_names, get_column_names  # Importar desde utils.py

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')

def generate_density_map(table_name, connection, column_name, background_table=None):
    """
    Generates a kernel density map from the specified table with an optional background layer.

    Args:
        table_name (str): Name of the table containing the polygon geometries.
        connection: Database connection object.
        column_name (str): Name of the column for density calculation.
        background_table (str, optional): Name of the table for the background layer.
    """
    try:
        # Sanitize the table name to avoid SQL injection
        table_name_sanitized = re.sub(r'[^A-Za-z0-9_ ]', '', table_name)

        # Ask for a value for the specified column
        column_value = input(f"Enter the value for column '{column_name}' (or press Enter to skip): ").strip()

        # Load geometry data from the polygon table with an optional filter on the column value
        if column_value:
            query = f'SELECT * FROM "{table_name_sanitized}" WHERE "{column_name}" = \'{column_value}\''
        else:
            query = f'SELECT * FROM "{table_name_sanitized}"'

        logging.info(f"Loading data from table {table_name_sanitized}")
        gdf = gpd.read_postgis(query, con=connection, geom_col='geom')

        # If a background table was provided, sanitize and load it
        if background_table:
            background_table_sanitized = re.sub(r'[^A-Za-z0-9_ ]', '', background_table)
            logging.info(f"Loading background data from table {background_table_sanitized}")
            gdf_background = gpd.read_postgis(f'SELECT * FROM "{background_table_sanitized}"', con=connection, geom_col='geom')

        # Calculate centroids of geometries that are not of Point type
        centroids = gdf.geometry.centroid
        coords = np.vstack([centroids.x, centroids.y]).T

        # Adjust the bandwidth for more accuracy
        kde = KernelDensity(bandwidth=0.1, kernel='gaussian')
        kde.fit(coords)

        # Increase the mesh resolution for more detail
        x_min, x_max = coords[:, 0].min() - 1, coords[:, 0].max() + 1
        y_min, y_max = coords[:, 1].min() - 1, coords[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500), np.linspace(y_min, y_max, 500))
        grid_coords = np.c_[xx.ravel(), yy.ravel()]

        # Evaluate the density at each point of the mesh
        Z = np.exp(kde.score_samples(grid_coords)).reshape(xx.shape)

        # Set the figure size to improve visibility
        fig, ax = plt.subplots(figsize=(12, 9))

        # If background polygons were loaded, plot them
        if background_table:
            gdf_background.plot(ax=ax, color='red', edgecolor='black')
            alpha_value = 0.8  # Use some transparency when there is a background
        else:
            alpha_value = 1.0  # Solid colors when there is no background

        # Plot the density as a heatmap over the background polygons
        cbar = ax.pcolormesh(xx, yy, Z, shading='auto', cmap='plasma', alpha=alpha_value)
        fig.colorbar(cbar, ax=ax, label=f'Density of {column_name}')

        # Load and display the logo in the lower left corner
        logo_path = 'garma.png'  # Ensure 'garma.png' is in the current directory
        if os.path.exists(logo_path):
            logging.info(f"Loading logo from {logo_path}")
            logo_img = mpimg.imread(logo_path)
            logo_ax = fig.add_axes([0.05, 0.05, 0.1, 0.1])  # Position and size of the logo on the plot
            logo_ax.imshow(logo_img)
            logo_ax.axis('off')
        else:
            logging.warning(f"Logo file {logo_path} not found. Skipping logo display.")

        # Adjust the plot limits to match the data limits
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_title('Kernel Density Map with Optional Background')

        # Ensure the 'figures' directory exists and save the figure there
        figures_dir = os.path.join(os.getcwd(), 'figures')
        os.makedirs(figures_dir, exist_ok=True)
        figure_path = os.path.join(figures_dir, 'kernel_density_map.png')
        plt.savefig(figure_path)
        logging.info(f"Kernel density map saved to {figure_path}")

        plt.show()

    except Exception as e:
        logging.error(f"Error generating density map: {e}")

# Función de prueba comentada para evitar ejecuciones no deseadas.
# connection = connect_to_db()
# if connection:
#     generate_density_map("your_table_name", connection, "your_column_name")
#     close_db_connection(connection)
