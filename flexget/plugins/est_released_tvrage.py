from __future__ import unicode_literals, division, absolute_import
import logging
from flexget.plugin import register_plugin
from flexget.plugins.api_tvrage import lookup_series

log = logging.getLogger('est_tvrage')


class EstimatesReleasedTVRage(object):

    def get_series_info(self, series_name):
        return lookup_series(name=series_name)

    def estimate(self, entry):
        if 'series_name' in entry and 'series_episode' in entry and 'series_season' in entry:
            season = entry['series_season']
            if entry.get('series_id_type') == 'sequence':
                # Tvrage has absolute numbered shows under season 1
                season = 1
            log.verbose("Querying release estimation for %s S%02dE%02d ..." %
                        (entry['series_name'], season, entry['series_episode']))
            series_info = self.get_series_info(entry['series_name'])
            if series_info is None:
                log.debug('No series info obtained from TVRage to %s' % entry['series_name'])
                return None
            try:
                episode_info = series_info.episode(season, entry['series_episode'])
                if episode_info:
                    return episode_info.airdate
            except Exception as e:
                log.exception(e)

            log.debug('No episode info obtained from TVRage for %s season %s episode %s' %
                      (entry['series_name'], entry['series_season'], entry['series_episode']))


register_plugin(EstimatesReleasedTVRage, 'est_released_tvrage', groups=['estimate_release'])
