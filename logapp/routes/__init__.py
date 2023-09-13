from litestar import Router

from logapp.routes.character import get_char_graph, get_image, pull_raid_hist_stats

character_router: Router = Router(
    path="/character", route_handlers=[pull_raid_hist_stats, get_char_graph, get_image]
)
