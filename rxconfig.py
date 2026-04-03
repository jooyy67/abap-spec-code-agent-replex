import reflex as rx

config = rx.Config(
    app_name="abap_spec_code_agent_reflex",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)