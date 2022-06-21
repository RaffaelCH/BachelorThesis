let input_source = document.getElementById('input-source');
let slider_colors = document.getElementById('slider-colors');
let slider_unknownfiles = document.getElementById('slider-unknownfiles');
let slider_generated = document.getElementById('slider-generated');
let slider_methods = document.getElementById('slider-methods');
let slider_errors = document.getElementById('slider-warnings');
let slider_separatewindows = document.getElementById('slider-separatewindows');

let label_slider_colors = document.getElementById('label-slider-colors');
let label_slider_unknownfiles = document.getElementById('label-slider-unknownfiles');
let label_slider_generated = document.getElementById('label-slider-generated');
let label_slider_methods = document.getElementById('label-slider-methods');
let label_slider_errors = document.getElementById('label-slider-warnings');
let label_slider_separatewindows = document.getElementById('label-slider-separatewindows');

var version = document.getElementById('manifest-version');
version.innerHTML = 'v' + chrome.app.getDetails().version;

input_source.onchange = event => {
  chrome.storage.local.set({ 'input-source': input_source.value });
}

slider_colors.onchange = event => {
  chrome.storage.local.set({ 'slider-colors': slider_colors.checked });
  updateSliderNames();
}

slider_unknownfiles.onchange = event => {
  chrome.storage.local.set({ 'slider-unknownfiles': slider_unknownfiles.checked });
  updateSliderNames();
}

slider_generated.onchange = event => {
  chrome.storage.local.set({ 'slider-generated': slider_generated.checked });
  updateSliderNames();
}

slider_methods.onchange = event => {
  chrome.storage.local.set({ 'slider-methods': slider_methods.checked });
  updateSliderNames();
}

slider_errors.onchange = event => {
  chrome.storage.local.set({ 'slider-warnings': slider_errors.checked });
  updateSliderNames();
}

slider_separatewindows.onchange = event => {
  chrome.storage.local.set({ 'slider-separatewindows': slider_separatewindows.checked });
  updateSliderNames();
}

chrome.storage.local.get(storage => {
  input_source.value = storage['input-source'];
  slider_colors.checked = storage['slider-colors'];
  slider_unknownfiles.checked = storage['slider-unknownfiles'];
  slider_generated.checked = storage['slider-generated'];
  slider_methods.checked = storage['slider-methods'];
  slider_errors.checked = storage['slider-warnings'];
  slider_separatewindows.checked = storage['slider-separatewindows'];
  updateSliderNames();
});

function updateSliderNames () {
  label_slider_colors.innerHTML = slider_colors.checked ? 'Package-based colors' : 'Change-based colors';
  label_slider_unknownfiles.innerHTML = slider_unknownfiles.checked ? 'Show nodes for unknown files' : 'Hide nodes for unknown files';
  label_slider_generated.innerHTML = slider_generated.checked ? 'Show generated nodes' : 'Hide generated nodes';
  label_slider_methods.innerHTML = slider_methods.checked ? 'Hide methods': 'Show methods';
  label_slider_errors.innerHTML = slider_errors.checked ? 'Show warnings' : 'Hide warnings';
  label_slider_separatewindows.innerHTML = slider_separatewindows.checked ? 'One window for all languages' : 'One window per language';
}
