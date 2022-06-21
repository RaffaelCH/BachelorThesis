var windowWidth = 1280, windowHeight = 720;

// Holds all active elements (windows, svgs, graphs).
// Keys have to be looked up using the language using languageKeys.
const languageSpecificElements = new Map();
languageSpecificElements.set('windows', new Map());
languageSpecificElements.set('svgs', new Map());
languageSpecificElements.set('graphs', new Map());


// Language names function as keys to languageSpecificElements.
// To enable combining languages as necessary (especially only one graph for all of them),
// languageKeys enables looking up the key used for each language to access the elements of this language.
const languageKeys = new Map();

function addKeyMatch (language, key) {
  languageKeys.set(language, key);
}

function getKeyMatch (language) {
  return languageKeys.get(language);
}

function deleteKeyMatch (language) {
  languageKeys.delete(language);
}


function getLanguageElement(elementType, language) {
  let key = getKeyMatch(language);
  languageSpecificElements.get(elementType).get(key);
}

function setLanguageElement (elementType, language, element) {
  let key = getKeyMatch(language);
  languageSpecificElements.get(elementType).set(key, element);
}


var errorWindow;


updateSettings();


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.data == undefined) {
    console.log('error retrieving data');
  } else {
    updateSettings();
  }
  return true;
});

chrome.storage.onChanged.addListener((item, area) => {
  var changedKey = Object.keys(item).filter(key => settings[key] != item[key].newValue).map(key => key)[0];
  settings[changedKey] = item[changedKey].newValue;
  if (changedKey == 'input-source') {
    getDataAndRedrawGraphs();
    // TODO: check for single/multiple windows.
  } else {
    languageSpecificElements.get('graphs').forEach(graph => graph.restart(changedKey))
  }
});

function updateSettings () {
  chrome.storage.local.get(
    storage => {
      settings = storage;
      getDataAndRedrawGraphs();
    });
}


function getDataAndRedrawGraphs () {

  var jsonUrl = settings['input-source'];

  if (jsonUrl == undefined) {
    return;
  }

  if (!jsonUrl.endsWith('.json')) {
    if (!jsonUrl.endsWith('/')) {
      jsonUrl += '/';
    }
    var splitted = location.href.split('/');
    jsonUrl += splitted[splitted.indexOf('merge_requests') + 1] + '.json';
  }

  chrome.runtime.sendMessage({ url: jsonUrl },
    response => {
      if (response.msg != undefined && response.msg.json != undefined) {
        if (errorWindow) {
          errorWindow.close();
        }
        initializeLanguagesAndRedrawGraphs(response.msg.json, response.msg.isCacheUpdated);
      }
      else {
        // TODO: Reset everything.
        let openWindows = languageSpecificElements.get('windows');
        openWindows.forEach(window => {window.close();});
        openWindows.clear();
        let errorDiv = document.createElement('div')
        errorDiv.setAttribute('class', 'error-div border-bottom');
        errorDiv.setAttribute('style', 'width:' + windowWidth + 'px;height:' + 50 + 'px;color:darkorange;text-align:center;');
        errorDiv.innerText = 'Error loading JSON.\nPlease check the connection URL.';
        errorWindow = window.open("", "_blank", "innerWidth=" + windowWidth + ",innerHeight=" + windowHeight);
        errorWindow.document.body.appendChild(errorDiv)
      }
    });
}


function initializeLanguagesAndRedrawGraphs (json, isCacheUpdated) {

  let languages = new Set((function* (nodes) {for (var node of nodes) {if (node.type != NodeType.UNKNOWNFILE) {yield node.language;}}})(json.nodes));

  // All language graphs are displayed in one single window.
  if (settings['slider-separatewindows']) {
    let combinedKey = Array.from(languages).join('+');
    languages.forEach(language => addKeyMatch(language, combinedKey));

    setupLanguageWindow(combinedKey);
    redrawLanguageSVG(combinedKey);

    if (isCacheUpdated == undefined || languageSpecificElements.get('graphs').get(combinedKey) == undefined) {
      let languageGraph = new Graph(json, languageSpecificElements.get('windows').get(combinedKey), languageSpecificElements.get('svgs').get(combinedKey));
      languageSpecificElements.get('graphs').set(combinedKey, languageGraph);
      languageGraph.start();
    }

    return;
  }
  
  // Open a new window for each language.
  languages.forEach(language => {

    // In the case of one element per language, the language name is the key.
    languageKey = language;
    addKeyMatch(languageKey, language);

    setupLanguageWindow(languageKey);
    redrawLanguageSVG(languageKey);

    let filteredData = {'nodes': [], 'links': []};
    filteredData.nodes = json.nodes.filter(node => node.language == language || node.type == NodeType.UNKNOWNFILE);
    let filteredNodesMap = new Map();
    filteredData.nodes.forEach(node => filteredNodesMap.set(node.id, node));
    filteredData.links = json.links.filter(link => filteredNodesMap.has(link.source) || filteredNodesMap.has(link.target));
    
    if (isCacheUpdated == undefined || languageSpecificElements.get('graphs').get(language) == undefined) {
      let languageGraph = new Graph(filteredData, languageSpecificElements.get('windows').get(language), languageSpecificElements.get('svgs').get(language));
      languageSpecificElements.get('graphs').set(language, languageGraph);
      languageGraph.start();
    }
  });
}


function setupLanguageWindow(languageKey) {
  var languageWindow = languageSpecificElements.get('windows').get(languageKey);

  if (!languageWindow || languageWindow.closed) {
    languageWindow = window.open("", "_blank", "innerWidth=" + windowWidth + ",innerHeight=" + windowHeight);
    languageSpecificElements.get('windows').set(languageKey, languageWindow);
  }
  else {
    languageWindow.document.body.innerHTML = '';
  }
  
  languageWindow.document.write('<html><head><title>Graph - ' + languageKey + ' </title></head><body style="margin: 0; display: flex; justify-content: center; align-items: center;"></body></html>');
  
  // update width and height to window with since it might already be open
  if (languageWindow.innerWidth > 0 && languageWindow.innerHeight > 0) {
    windowWidth = languageWindow.innerWidth;
    windowHeight = languageWindow.innerHeight;
  }

  addLanguageSelectorStyleSheet(languageWindow);
  addErrorWindowStyleSheet(languageWindow);

  d3.select(languageWindow.document.body)
    .on("keydown", event => {
      isClickExpand = d3.event.key == "Shift";
      if (d3.event.key == 'Control') {
        isHighlightLocked = isHovering && !isHighlightLocked ? true : false;
        if (!isHighlightLocked && !isHovering) {
          let graph = languageSpecificElements.get('graphs').get(languageKey);
          graph._onHoverExit();
        }
      }
      else if (d3.event.key == 'Shift') {
        isClickExpand = true; // needs to be reset (currently done in graph)
      }
    });
}


function redrawLanguageSVG (languageKey) {
  let languageSvg = languageSpecificElements.get('svgs').get(languageKey);
  let languageWindow = languageSpecificElements.get('windows').get(languageKey);

  if (languageSvg != undefined) {
    languageSvg.remove();
  }

  languageSvg = d3.select(languageWindow.document.body)
    .append('svg')
    .attr('id', 'graph')
    .attr('width', windowWidth).attr('height', windowHeight)
    .style('cursor', 'move');

  languageSpecificElements.get('svgs').set(languageKey, languageSvg);

  languageWindow.addEventListener("resize", e => windowResize(languageKey, e));
  languageWindow.onbeforeunload = () => cleanUpResources(languageKey);
}


function windowResize (languageKey, event) {
  event.preventDefault();

  let languageWindow = languageSpecificElements.get('windows').get(languageKey);
  let languageSvg = languageSpecificElements.get('svgs').get(languageKey);
  let languageGraph = languageSpecificElements.get('graphs').get(languageKey);

  languageSvg.attr('width', languageWindow.innerWidth);
  languageSvg.attr('height', languageWindow.innerHeight);

  if (languageGraph != undefined) {
    languageGraph.updateForceCenter();
  }
}


// Remove all objects for a certain languageKey.
// Windows get closed and simulations stopped.
// Also removes all references to these objects.
function cleanUpResources(languageKey) {
  let languageWindow = languageSpecificElements.get('windows').get(languageKey);
  let languageGraph = languageSpecificElements.get('graphs').get(languageKey);

  languageWindow.close();
  languageGraph.simulation.stop();

  languageSpecificElements.get('windows').delete(languageKey);
  languageSpecificElements.get('svgs').delete(languageKey);
  languageSpecificElements.get('graphs').delete(languageKey);
}