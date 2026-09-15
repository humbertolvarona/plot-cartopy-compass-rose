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
    ax.add_patch(mpatches.Circle((lon, lat), inner_r, fill=False, color='lightgray', linewidth=0.5, transform=transform,
                                 zorder=11))


    for angle in [0, 90, 180, 270]:
        ax.plot([lon, lon + inner_r * np.cos(np.radians(angle))], [lat, lat + inner_r * np.sin(np.radians(angle))],
                color='lightgray', linewidth=0.5, transform=transform, zorder=11)


    for angle in [45, 135, 225, 315]:
        ax.plot([lon, lon + 0.4 * inner_r * np.cos(np.radians(angle))],
                [lat, lat + 0.4 * inner_r * np.sin(np.radians(angle))], color='lightgray', linewidth=0.5,
                transform=transform, zorder=11)


    arrow_r = 0.8 * r

    north_arrow_tip = mpatches.Polygon([[lon, lat + arrow_r], [lon - 0.1 * arrow_r, lat], [lon + 0.1 * arrow_r, lat]],
                                       color='darkgray', transform=transform, zorder=12)
    ax.add_patch(north_arrow_tip)

    north_red_tip = mpatches.Polygon([[lon, lat + arrow_r], [lon - 0.05 * arrow_r, lat + 0.8 * arrow_r],
                                      [lon + 0.05 * arrow_r, lat + 0.8 * arrow_r]], color='darkred',
                                     transform=transform, zorder=13)
    ax.add_patch(north_red_tip)


    south_arrow = mpatches.Polygon([[lon, lat - arrow_r], [lon - 0.1 * arrow_r, lat], [lon + 0.1 * arrow_r, lat]],
                                   color='darkgray', transform=transform, zorder=12)
    ax.add_patch(south_arrow)
    east_arrow = mpatches.Polygon([[lon + arrow_r, lat], [lon, lat + 0.1 * arrow_r], [lon, lat - 0.1 * arrow_r]],
                                  color='darkgray', transform=transform, zorder=12)
    ax.add_patch(east_arrow)
    west_arrow = mpatches.Polygon([[lon - arrow_r, lat], [lon, lat + 0.1 * arrow_r], [lon, lat - 0.1 * arrow_r]],
                                  color='darkgray', transform=transform, zorder=12)
    ax.add_patch(west_arrow)


    sec_arrow_r = 0.5 * r
    for angle in [45, 135, 225, 315]:
        arrow = mpatches.Polygon(
            [[lon + sec_arrow_r * np.cos(np.radians(angle)), lat + sec_arrow_r * np.sin(np.radians(angle))],
             [lon + 0.05 * sec_arrow_r * np.cos(np.radians(angle - 10)),
              lat + 0.05 * sec_arrow_r * np.sin(np.radians(angle - 10))],
             [lon + 0.05 * sec_arrow_r * np.cos(np.radians(angle + 10)),
              lat + 0.05 * sec_arrow_r * np.sin(np.radians(angle + 10))]],
            color='darkgray', transform=transform, zorder=12)
        ax.add_patch(arrow)


    text_r = 1.2 * r
    ax.text(lon, lat + text_r, 'N', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color='darkred', zorder=15)
    ax.text(lon, lat - text_r, 'S', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color='black', zorder=15)
    ax.text(lon + text_r, lat, 'E', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color='black', zorder=15)
    ax.text(lon - text_r, lat, 'W', transform=transform, ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color='black', zorder=15)
