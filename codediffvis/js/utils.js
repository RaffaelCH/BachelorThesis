var remToPixelMap = new Map();

remToPixel = rem => {
    if (remToPixelMap.has(rem)) {
        return remToPixelMap.get(rem);
    }
    const pixel = Math.round(rem * parseFloat(getComputedStyle(document.documentElement).fontSize));
    remToPixelMap.set(rem, pixel);
    return pixel;
}


addLanguageSelectorStyleSheet = (targetWindow) => {
		
    var languageSelectorStyleSheetElement;

    for (const sheet of targetWindow.document.styleSheets) {
        if (sheet.title === 'languageSelectorSheet') {
            languageSelectorStyleSheetElement = sheet;
            break;
        }
    }

    if (!Boolean(languageSelectorStyleSheetElement)) {
        languageSelectorStyleSheetElement = document.createElement('style');
        languageSelectorStyleSheetElement.title = 'languageSelectorSheet';
        targetWindow.document.body.appendChild(languageSelectorStyleSheetElement);
        
        let sheet = languageSelectorStyleSheetElement.sheet;
        sheet.insertRule('.slider:before { position: absolute; content: ""; height: 0.75rem; width: 0.75rem; left: 0.125rem; bottom: 0.125rem; background-color: white; transition: .3s; }', 0);
        sheet.insertRule('input:focus+.slider { box-shadow: 0 0 1px #ccc; }', 1);
        sheet.insertRule('input:checked+.slider:before { transform: translateX(1rem); background-color: #333; }', 2);
    }
}


addErrorWindowStyleSheet = (targetWindow) => {
	
    var errorWindowStyleSheetElement;

    for (const sheet of targetWindow.document.styleSheets) {
        if (sheet.title === 'errorWindowSheet') {
            errorWindowStyleSheetElement = sheet;
            break;
        }
    }

    if (!Boolean(errorWindowStyleSheetElement)) {
        errorWindowStyleSheetElement = document.createElement('style');
        errorWindowStyleSheetElement.title = 'errorWindowSheet';
        targetWindow.document.body.appendChild(errorWindowStyleSheetElement);
        
        let sheet = errorWindowStyleSheetElement.sheet;
        sheet.insertRule('.close-button:after { display: inline-block; content: "x"; }', 0);
    }
}