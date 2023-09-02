from litestar import Router

from logapp.routes.character import pull_raid_hist_stats

character_router: Router = Router(
    path="/char-raid-stats", route_handlers=[pull_raid_hist_stats]
)
