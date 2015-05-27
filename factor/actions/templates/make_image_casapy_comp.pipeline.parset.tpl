pipeline.steps=[casapy]

casapy.control.kind=recipe
casapy.control.type=casapy
casapy.control.opts.mapfiles_in=[{{ vis_datamap }}, {{ output_datamap }}, {{ completed_datamap }}]
casapy.control.opts.inputkeys=[inputms, outputimage, completedfile]
casapy.control.opts.arguments=[--nologger, -c, {{ scriptname }}, inputms, outputimage, completedfile]
casapy.control.opts.max_per_node={{ n_per_node }}