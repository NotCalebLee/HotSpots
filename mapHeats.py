import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load final placed data
dart_df = pd.read_csv(r"C:\Users\lunes\Documents\Wifi-map\outputs\dartmouth_placed_windowed_dedup_jan2015.csv")
hk_df   = pd.read_csv(r"C:\Users\lunes\Documents\Wifi-map\outputs\hk_placed_windowed_dedup_jan2015.csv")

# Helper plotting function
def plot_heatmap(df, title, out_path):
    plt.figure(figsize=(8,6))
    sns.kdeplot(
        x=df["lon"], y=df["lat"],
        cmap="Reds", shade=True, fill=True, thresh=0.05
    )
    plt.scatter(df["lon"], df["lat"], s=10, alpha=0.3, c="black")
    plt.title(title, fontsize=14)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.show()

# Plot Dartmouth heatmap
plot_heatmap(dart_df, "Dartmouth Wi-Fi Heat Map (Jan 2015)", r"C:\Users\lunes\Documents\Wifi-map\outputs\dart_heatmap.png")

# Plot Hong Kong heatmap
plot_heatmap(hk_df, "HK Wi-Fi Heat Map (Jan 2015)", r"C:\Users\lunes\Documents\Wifi-map\outputs\hk_heatmap.png")

# Prepare HK data
hk_3d = hk_df.dropna(subset=["lat", "lon", "Floor"])
hk_3d["Floor"] = hk_3d["Floor"].astype(float)

# Plot 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# color by floor for clarity
sc = ax.scatter(
    hk_3d["lon"], hk_3d["lat"], hk_3d["Floor"],
    c=hk_3d["Floor"], cmap='plasma', s=20, alpha=0.6
)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Floor')
ax.set_title('Hong Kong Wi-Fi 3D Building Heat Map (Jan 2015)')

fig.colorbar(sc, ax=ax, label='Floor')
plt.tight_layout()
plt.savefig(r"C:\Users\lunes\Documents\Wifi-map\outputs\hk_3d_heatmap.png", dpi=300)
plt.show()
