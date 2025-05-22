import cufflinks as cf

def configure_cufflinks():
    """Configures cufflinks for offline use."""
    cf.go_offline()
    cf.set_config_file(offline=True, world_readable=False)