import traceback
from io import StringIO
from contextlib import redirect_stdout

import gradio as gr
from modules import script_callbacks, shared
from modules.ui_components import ResizeHandleRow

def execute(code):
    io = StringIO()
    
    with redirect_stdout(io):
        try:
            exec(code)
        except Exception:
            trace = traceback.format_exc().split('\n')
            del trace[2]
            del trace[1]

            print('\n'.join(trace))

    return io.getvalue()

def warn_allow_code():
    gr.Warning('UI was not launched with --allow-code flag')
    return "⚠️ Code could not be executed. Please relaunch the UI with the --allow-code flag enabled"

def create_code_tab(language, input_default, output_default, lines):
    with gr.Tab(language.capitalize(), elem_id=f"qic-{language}-tab"):
        with gr.Row(), ResizeHandleRow(equal_height=False):
            with gr.Column(scale=1):
                inp = gr.Code(value=input_default, language=language, label=f"{language.capitalize()} code", lines=lines, elem_id=f"qic-{language}-input", elem_classes="qic-console")
                btn = gr.Button("Run", variant='primary', elem_id=f"qic-{language}-submit")
            
            with gr.Column(scale=1):
                out = gr.Code(value=output_default, language=language if getattr(shared.opts, f'qic_use_syntax_highlighting_{language}_output') else None, label="Output", lines=lines, interactive=False, elem_id=f"qic-{language}-output", elem_classes="qic-console")
        
        if not shared.cmd_opts.allow_code:
            btn.click(fn=warn_allow_code, inputs=None, outputs=out)
        elif language == "python":
            btn.click(fn=execute, inputs=inp, outputs=out)
        else:
            btn.click(fn=lambda x: x, _js="qic.execute", inputs=inp, outputs=out)


def on_ui_tabs():
    with gr.Blocks(elem_id="qic-root", analytics_enabled=False) as ui_component:
        if not shared.opts.qic_hide_warning:
                gr.Markdown("""# ⚠️ WARNING ⚠️
This extension was made for developers! If someone ever asks you to install this extension and run any code they send you, **DON'T**. There are no safety checks in place, and malicious code can be ran without restriction.

In order for code here to be executable the UI must be launched with the `--allow-code` flag.

This warning message can be disabled in `Settings > QIC Console > Hide warning message`""")
        
        create_code_tab("python", "import gradio as gr\nfrom modules import shared, scripts\n\nprint(f\"Current loaded checkpoint is {shared.opts.sd_model_checkpoint}\")", "# Output will appear here\n\n# Tip: Press `ctrl+space` to execute the current code", shared.opts.qic_default_num_lines)
        create_code_tab("javascript", "const app = gradioApp();\n\nconsole.log(`A1111 is running on ${gradio_config.root}`)", "// Output will appear here\n\n// Tip: Press `ctrl+space` to execute the current code", shared.opts.qic_default_num_lines)

        return [(ui_component, "QIC Console", "qic-console")]


def on_ui_settings():
    settings_section = ('qic-console', "QIC Console")
    options = {
        "qic_use_syntax_highlighting_python_output": shared.OptionInfo(True, "Use syntax highlighting on Python output console", gr.Checkbox).needs_reload_ui(),
        "qic_use_syntax_highlighting_javascript_output": shared.OptionInfo(True, "Use syntax highlighting on Javascript output console", gr.Checkbox).needs_reload_ui(),
        "qic_default_num_lines": shared.OptionInfo(30, "Default number of console lines", gr.Number, {"precision": 0}).needs_reload_ui(),
        "qic_hide_warning": shared.OptionInfo(False, "Hide warning message", gr.Checkbox).needs_reload_ui(),
    }

    for name, opt in options.items():
        opt.section = settings_section
        shared.opts.add_option(name, opt)


script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_ui_settings(on_ui_settings)
