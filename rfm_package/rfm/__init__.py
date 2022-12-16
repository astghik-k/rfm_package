"""Top-level package for RFM Package."""

__author__ = """Astghik Kostanyan"""
__email__ = 'kostanyan.astghik@gmail.com'
__version__ = '0.1.0'

from rfm_package.rfm.main import (create_rfm_columns,
                                  scale_rfm_columns,
                                  rfm_scores,
                                  give_names_to_segments,
                                  segments_distribution,
                                  visualize_segments,
                                  plot_rfm)
