# Cartopy Detailed Compass Rose

This document provides a comprehensive explanation of the custom implementation designed to render a highly detailed compass rose within Cartopy geographic visualizations.

## General Description

The function draw_detailed_compass generates a vector-based compass rose directly on a Cartopy geographical axes object. The visual structure incorporates an outer beveled circle segmented into sixteen sectors with alternating grayscale tones. Internally, the design features a secondary circle containing orthogonal and diagonal reference lines. The principal cardinal directions are indicated by complex beveled arrows, emphasizing the northern direction with a dark red apex. Secondary intercardinal arrows provide supplementary spatial orientation. The cardinal typography employs bold characters positioned at the outer boundaries, strictly matching the dark red color for the northern indicator. The construction utilizes Matplotlib geometric patches, such as Wedge, Circle, and Polygon, guaranteeing optimal scaling and rendering fidelity across various resolutions.

## Implementation in Python 3.14

```python
def draw_detailed_compass(ax, lon, lat, scale, fontsize, transform):
    r = scale
    num_sectors = 16
    for i in range(num_sectors):
        theta1 = i * (360 / num_sectors)
        theta2 = (i + 1) * (360 / num_sectors)
        color = 'lightgray' if i % 2 == 0 else 'darkgray'
        wedge = mpatches.Wedge((lon, lat), r, theta1, theta2, color=color, alpha=0.8, transform=transform, zorder=10)
        ax.add_patch(wedge)
    inner_r = 0.6 * r
    ax.add_patch(mpatches.Circle((lon, lat), inner_r, fill=False, color='lightgray', linewidth=0.5, transform=transform, zorder=11))
    for angle in [0, 90, 180, 270]:
        ax.plot([lon, lon + inner_r * np.cos(np.radians(angle))], [lat, lat + inner_r * np.sin(np.radians(angle))], color='lightgray', linewidth=0.5, transform=transform, zorder=11)
    for angle in [45, 135, 225, 315]:
        ax.plot([lon, lon + 0.4 * inner_r * np.cos(np.radians(angle))], [lat, lat + 0.4 * inner_r * np.sin(np.radians(angle))], color='lightgray', linewidth=0.5, transform=transform, zorder=11)
    arrow_r = 0.8 * r
    north_arrow_tip = mpatches.Polygon([[lon, lat + arrow_r], [lon - 0.1 * arrow_r, lat], [lon + 0.1 * arrow_r, lat]], color='darkgray', transform=transform, zorder=12)
    ax.add_patch(north_arrow_tip)
    north_red_tip = mpatches.Polygon([[lon, lat + arrow_r], [lon - 0.05 * arrow_r, lat + 0.8 * arrow_r], [lon + 0.05 * arrow_r, lat + 0.8 * arrow_r]], color='darkred', transform=transform, zorder=13)
    ax.add_patch(north_red_tip)
    south_arrow = mpatches.Polygon([[lon, lat - arrow_r], [lon - 0.1 * arrow_r, lat], [lon + 0.1 * arrow_r, lat]], color='darkgray', transform=transform, zorder=12)
    ax.add_patch(south_arrow)
    east_arrow = mpatches.Polygon([[lon + arrow_r, lat], [lon, lat + 0.1 * arrow_r], [lon, lat - 0.1 * arrow_r]], color='darkgray', transform=transform, zorder=12)
    ax.add_patch(east_arrow)
    west_arrow = mpatches.Polygon([[lon - arrow_r, lat], [lon, lat + 0.1 * arrow_r], [lon, lat - 0.1 * arrow_r]], color='darkgray', transform=transform, zorder=12)
    ax.add_patch(west_arrow)
    sec_arrow_r = 0.5 * r
    for angle in [45, 135, 225, 315]:
        arrow = mpatches.Polygon([[lon + sec_arrow_r * np.cos(np.radians(angle)), lat + sec_arrow_r * np.sin(np.radians(angle))], [lon + 0.05 * sec_arrow_r * np.cos(np.radians(angle - 10)), lat + 0.05 * sec_arrow_r * np.sin(np.radians(angle - 10))], [lon + 0.05 * sec_arrow_r * np.cos(np.radians(angle + 10)), lat + 0.05 * sec_arrow_r * np.sin(np.radians(angle + 10))]], color='darkgray', transform=transform, zorder=12)
        ax.add_patch(arrow)
    text_r = 1.2 * r
    ax.text(lon, lat + text_r, 'N', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold', color='darkred', zorder=15)
    ax.text(lon, lat - text_r, 'S', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold', color='black', zorder=15)
    ax.text(lon + text_r, lat, 'E', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold', color='black', zorder=15)
    ax.text(lon - text_r, lat, 'W', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold', color='black', zorder=15)
```

## Requirements

The execution of this module requires a Python 3.14 environment. The fundamental dependencies encompass Matplotlib for the instantiation of the geometric patches and textual elements. Cartopy is strictly necessary for the definition of the map projections and the coordinate reference systems invoked during geometric transformations. Numpy is required for the trigonometric calculations applied in the vertex definition of the radial and secondary arrows. Additionally, the standard ssl library must be configured to bypass certificate verification during the retrieval of the Natural Earth physical features.

## Examples

The first example applies the function over a South Polar Stereographic projection. This configuration defines three independent panels visualizing the Antarctic continent from distinct longitudinal perspectives, including the southern sectors of America, Africa, and Australia. The compass rose is placed in the superior right quadrant of each panel, utilizing the Plate Carree projection as the local coordinate reference system for the drawing.

```python
import ssl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

fig = plt.figure(figsize=(24, 8))
projection = ccrs.SouthPolarStereo()
coastline = cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
compass_scale = 3
compass_fontsize = 16

ax1 = fig.add_subplot(1, 3, 1, projection=projection)
ax1.set_extent([-90, -50, -80, -25], crs=ccrs.PlateCarree())
ax1.add_feature(coastline)
gl1 = ax1.gridlines(draw_labels=True, linewidth=0.8, color='lightgray', alpha=0.8, linestyle=':')
gl1.top_labels = False
gl1.right_labels = False
gl1.xlabel_style = {'size': 12, 'weight': 'bold'}
gl1.ylabel_style = {'size': 12, 'weight': 'bold'}
gl1.xformatter = LongitudeFormatter(zero_direction_label=True, number_format='.0f')
gl1.yformatter = LatitudeFormatter(number_format='.0f')
draw_detailed_compass(ax1, -55, -30, compass_scale, compass_fontsize, ccrs.PlateCarree())

ax2 = fig.add_subplot(1, 3, 2, projection=projection)
ax2.set_extent([10, 50, -80, -25], crs=ccrs.PlateCarree())
ax2.add_feature(coastline)
gl2 = ax2.gridlines(draw_labels=True, linewidth=0.8, color='lightgray', alpha=0.8, linestyle=':')
gl2.top_labels = False
gl2.right_labels = False
gl2.xlabel_style = {'size': 12, 'weight': 'bold'}
gl2.ylabel_style = {'size': 12, 'weight': 'bold'}
gl2.xformatter = LongitudeFormatter(zero_direction_label=True, number_format='.0f')
gl2.yformatter = LatitudeFormatter(number_format='.0f')
draw_detailed_compass(ax2, 45, -30, compass_scale, compass_fontsize, ccrs.PlateCarree())

ax3 = fig.add_subplot(1, 3, 3, projection=projection)
ax3.set_extent([110, 160, -80, -10], crs=ccrs.PlateCarree())
ax3.add_feature(coastline)
gl3 = ax3.gridlines(draw_labels=True, linewidth=0.8, color='lightgray', alpha=0.8, linestyle=':')
gl3.top_labels = False
gl3.right_labels = False
gl3.xlabel_style = {'size': 12, 'weight': 'bold'}
gl3.ylabel_style = {'size': 12, 'weight': 'bold'}
gl3.xformatter = LongitudeFormatter(zero_direction_label=True, number_format='.0f')
gl3.yformatter = LatitudeFormatter(number_format='.0f')
draw_detailed_compass(ax3, 155, -15, compass_scale, compass_fontsize, ccrs.PlateCarree())

plt.savefig('example_1.jpeg', dpi=500, bbox_inches='tight')
plt.show()
```

The second example utilizes the Plate Carree projection to visualize a global map. The compass rose is instantiated in the equatorial zone over the Atlantic Ocean, demonstrating the spatial accuracy of the vector drawing within an equidistant cylindrical projection. The graphical procedure processes the input coordinates avoiding structural deformation.

```python
import ssl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

fig2 = plt.figure(figsize=(12, 6))
projection2 = ccrs.PlateCarree()
ax_global = fig2.add_subplot(1, 1, 1, projection=projection2)
ax_global.set_global()
coastline_global = cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
ax_global.add_feature(coastline_global)

gl_global = ax_global.gridlines(draw_labels=True, linewidth=0.8, color='lightgray', alpha=0.8, linestyle=':')
gl_global.top_labels = False
gl_global.right_labels = False
gl_global.xlabel_style = {'size': 12, 'weight': 'bold'}
gl_global.ylabel_style = {'size': 12, 'weight': 'bold'}
gl_global.xformatter = LongitudeFormatter(zero_direction_label=True, number_format='.0f')
gl_global.yformatter = LatitudeFormatter(number_format='.0f')

draw_detailed_compass(ax_global, -30, 0, 10, 12, ccrs.PlateCarree())
plt.savefig('example_2.jpeg', dpi=500, bbox_inches='tight')
plt.show()
```

The third example applies the Orthographic projection, generating an external perspective of the Earth. This configuration positions the compass rose near the periphery of the visible hemisphere. The execution confirms the robust transformation of the geometric patches across non-cylindrical coordinate systems.

```python
import ssl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

fig3 = plt.figure(figsize=(8, 8))
projection3 = ccrs.Orthographic(central_longitude=-45.0, central_latitude=-20.0)
ax_ortho = fig3.add_subplot(1, 1, 1, projection=projection3)
ax_ortho.set_global()
coastline_ortho = cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
ax_ortho.add_feature(coastline_ortho)

gl_ortho = ax_ortho.gridlines(draw_labels=False, linewidth=0.8, color='lightgray', alpha=0.8, linestyle=':')

draw_detailed_compass(ax_ortho, -20, 20, 5, 10, ccrs.PlateCarree())
plt.savefig('example_3.jpeg', dpi=500, bbox_inches='tight')
plt.show()
```

## License

This document and the associated code are distributed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). Any reproduction, modification, or distribution must obligatorily acknowledge its creator, __Humberto Lazaro Varona Gonzalez__, providing the corresponding credit and indicating if modifications were made.

**Author:** HL Varona

[**Profile:**](https://scholar.google.com/citations?user=QOQCC6AAAAAJ)

