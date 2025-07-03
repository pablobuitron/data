import os
import geopandas as gpd
import rasterio
import xarray as xr
import matplotlib.pyplot as plt

# Diccionarios de almacenamiento
vector_data = {}
raster_data = {}
netcdf_data = {}

# Ruta base (como estás en data/, es ".")
base_dir = "."

# Extensiones por tipo
vector_exts = ['.shp']
raster_exts = ['.tif', '.tf', '.adf']
netcdf_exts = ['.nc']

# Función auxiliar para encontrar archivos
def find_files(base, extensions):
    for root, dirs, files in os.walk(base):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                yield os.path.join(root, file)

# 📦 Cargar vectoriales (.shp)
for shp_file in find_files(base_dir, vector_exts):
    try:
        # Ruta relativa como nombre clave
        rel_path = os.path.relpath(shp_file, base_dir)
        name = rel_path.replace(os.sep, "_").replace(".shp", "")
        gdf = gpd.read_file(shp_file)
        vector_data[name] = gdf
        print(f"✔️ Vector cargado: {name} | {gdf.shape[0]} registros")
    except Exception as e:
        print(f"❌ Error cargando vectorial {shp_file}: {e}")

# 🗺️ Cargar raster (.tif, .tf, .adf)
for raster_file in find_files(base_dir, raster_exts):
    try:
        rel_path = os.path.relpath(raster_file, base_dir)
        name = rel_path.replace(os.sep, "_").split(".")[0]
        src = rasterio.open(raster_file)
        raster_data[name] = src
        print(f"🗺️ Raster cargado: {name} | shape: {src.width}x{src.height}")
    except Exception as e:
        print(f"❌ Error cargando raster {raster_file}: {e}")

# 🌡️ Cargar netCDF (.nc)
for nc_file in find_files(base_dir, netcdf_exts):
    try:
        rel_path = os.path.relpath(nc_file, base_dir)
        name = rel_path.replace(os.sep, "_").replace(".nc", "")
        ds = xr.open_dataset(nc_file)
        netcdf_data[name] = ds
        print(f"🌡️ NetCDF cargado: {name} | variables: {list(ds.variables)}")
    except Exception as e:
        print(f"❌ Error cargando netCDF {nc_file}: {e}")

# 👀 Mostrar todos los vectoriales cargados
print("\n🔍 Claves disponibles en vector_data:")
for k in vector_data:
    print(f" - {k}")

# ✅ Ejemplo: mostrar uno y graficar
clave_ejemplo = list(vector_data.keys())[0]  # usa el primero que se cargó
suelo = vector_data[clave_ejemplo]
print(f"\nMostrando: {clave_ejemplo}")
print(suelo.head())

# Graficar
suelo.plot()
plt.title(clave_ejemplo)
plt.tight_layout()
plt.show()
