from litestar import Router

from logapp.routes.character import (
    get_char_graph,
    get_info_image,
    get_logs_dungs_image,
    get_logs_raid_image,
    pull_raid_hist_stats,
)

character_router: Router = Router(
    path="/character",
    route_handlers=[
        pull_raid_hist_stats,
        get_char_graph,
        get_info_image,
        get_logs_raid_image,
        get_logs_dungs_image,
    ],
)
