from pysvelte.svelte_component import SvelteComponent


def refresh():
    for component in SvelteComponent.autogenerate():
        globals()[component.name] = component
        __all__.append(component.name)

__all__ = ["SvelteComponent"]
refresh()