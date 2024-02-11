(function(qic){
    const app = gradioApp();

    function throwError(){
        return new Error();
    }

    qic.injectUI = function(){
        document.addEventListener('keydown', function(e) {
            if(app.getElementById('tab_qic-console').style.display == 'block' && e.ctrlKey && e.key === ' '){
                const activeConsole = app.getElementById('qic-python-tab').parentElement.querySelector(".tab-nav .selected").innerText.toLowerCase();
                app.getElementById(`qic-${activeConsole}-submit`).click();
                e.preventDefault();
            }
        });
    }

    qic.execute = function(input){
        function getEvalSource(error){
            const lineMatch = [...error.stack.matchAll(/(?:eval|<?anonymous>?):(\d+):(\d+)/ig)][0]; // FF and Chrome
    
            if(lineMatch){
                return ` @ line ${lineMatch[1]}:${lineMatch[2]}`;
            }
    
            return " @ unknown location"
        }

        const formatLogValues = (...args) => `${args.join(' ')} ${getEvalSource(throwError())}`;
        
        let logs = [];

        const originalLog = console.log;
        const originalWarn = console.warn;
        const originalError = console.error;

        console.log = (...args) => logs.push({type: 'log', value: formatLogValues(...args)});
        console.warn = (...args) => logs.push({type: 'warning', value: formatLogValues(...args)});
        console.error = (...args) => logs.push({type: 'error', value: formatLogValues(...args)});

        try{
            eval(input);
        } catch(error){
            logs.push({type: 'error', value: `${error} ${getEvalSource(error)}`});
        }
         
        console.log = originalLog;
        console.warn = originalWarn;
        console.error = originalError;

        return logs.map(e => `[${e.type}]${' '.repeat(8 - e.type.length)}${e.value}`).join('\n');
    }

    onUiLoaded(qic.injectUI);

})(window.qic = window.qic || {});