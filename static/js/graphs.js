/**
 * Set-up given element to display a pie chart with the given data
 * @param {HTMLElement} element Container to render graph in
 * @param {Object} dataset Data to be rendered to the graph
 * @param {String} name Unique identifier for the graph
 * @param {String} type Graph type to display as
 * @param {Object} customSettings Additional chart.js settings specific to this graph
 */
function setToGraph(element, dataset, name, type, customSettings=null) {
    if (customSettings === null) {
        customSettings = {}
    }
    if (element.tagName.toLowerCase() !== 'div') {
        throw Error('Element must be of type "div"')
    }

    let canvas = document.createElement('canvas');
    canvas.id = name;
    element.appendChild(canvas);
    generateGraph(canvas, name, dataset, type, customSettings);
}

/**
 * Generate graph on given element with given parameters
 * @param {HTMLCanvasElement} element Canvas to render graph in
 * @param {String} name Unique identifier for the graph
 * @param {Object} dataset Data to be rendered to the graph
 * @param {String} type Type of graph to be displayed
 * @param {Object} customSettings Additional chart.js settings specific to this graph
 */
function generateGraph(element, name, dataset, type, customSettings) {
    let colorDefinition = dataset['color'];
    let color;
    if (colorDefinition === undefined) {
        color = generateColorsRandomSeeded(dataset["label"]);
    } else {
        switch (colorDefinition['type']) {
            case 'list': // Map colors using provided list
                color = colorDefinition['value'];
                break;
            case 'gradient': // Generate colors along provided gradient
                // Get suggested min and max from settings if present
                let ticks = ((((customSettings['options'] || {})['scales'] || {})['yAxes'] || [{}])[0]['ticks'] || {});
                color = generateColorsGradient(
                    dataset.data,
                    ticks['suggestedMin'] || 0, ticks['suggestedMax'] || 0,
                    colorDefinition['gradient']
                );
                break;
        }
    }
    // Default settings for the chart.js graphs
    let config = {
        type: type,
        data: {
            datasets: [{
                data: dataset.data,
                backgroundColor: color,
                label: ""
            }],
            labels: dataset.label
        },
        options: {
            title: {
                display: true,
                text: name
            },
            responsive: true,
            scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 0
                    }
                }]
            }
        }
    }
    merge(config, customSettings);

    let ctx = element.getContext('2d');
    window[name] = new Chart(ctx, config);
}

/**
 * Randomly generate list of colors, each seeded corresponding indexes of the given list
 * @param {Array.<String>} seeds List of rng seeds to apply to each color
 * @returns {Array.<String>} List of hex string colors of same length as seeds list
 */
function generateColorsRandomSeeded(seeds) {
    let colors = [];
    let r, g, b, rng;
    for (let seed of seeds) {
        rng = new Math.seedrandom(generateHash(seed));
        // Generate rgb values for the color
        r = "0" + generate(0, 255, rng).toString(16);
        g = "0" + generate(0, 255, rng).toString(16);
        b = "0" + generate(0, 255, rng).toString(16);
        // Convert rgb to hex string
        colors.push('#'
            + r.substring(r.length - 2, r.length)
            + g.substring(g.length - 2, g.length)
            + b.substring(b.length - 2, b.length));
    }
    return colors;
}

/**
 * Take the given array of numbers and produce an equal length array of hex colors, with
 * each color mapped according to the relative value of each corresponding value.
 * @param {Array.<Number>} data List of values to be mapped to colors
 * @param {Number} min Minimum possible value (can be overriden by data)
 * @param {Number} max Maximum possible value (can be overriden by data)
 * @param {Array.<String>} gradient Array of hex colors to gradiate evenly between
 */
function generateColorsGradient(data, min, max, gradient) {
    // Override max and min if larger/smaller values exist within the data
    min = Math.min(Math.min(...data), min);
    max = Math.max(Math.max(...data), max);
    // Value range of each gradient block
    let threshold = (max - min) / (gradient.length - 1);

    let colors = [];
    let r, g, b, redStart, greenStart, blueStart, redEnd, greenEnd, blueEnd, redDelta, greenDelta, blueDelta, startColor, endColor;
    for (let value of data) {
        // Identify which gradient block the current value is in
        let index = 0;
        for (let i = 0; i < gradient.length; i++) {
            if (value - min > threshold * i) {
                index = i;
            } else {
                break;
            }
        }
        // Get and parse the start and end colors for the current gradient block
        startColor = gradient[index];
        endColor = gradient[index + 1];

        redStart = parseInt(startColor.substring(1, 3), 16);
        redEnd = parseInt(endColor.substring(1, 3), 16);
        redDelta = (redEnd - redStart);

        greenStart = parseInt(startColor.substring(3, 5), 16);
        greenEnd = parseInt(endColor.substring(3, 5), 16);
        greenDelta = (greenEnd - greenStart);

        blueStart = parseInt(startColor.substring(5, 7), 16);
        blueEnd = parseInt(endColor.substring(5, 7), 16);
        blueDelta = (blueEnd - blueStart);

        // Normalise the given value into the rgb range of the current gradient block
        r = redStart + (specialMod((value - min), (threshold)) * redDelta / threshold);
        g = greenStart + (specialMod((value - min), (threshold)) * greenDelta / threshold);
        b = blueStart + (specialMod((value - min), (threshold)) * blueDelta / threshold);

        // Convert the rgb values to hex string equivalent
        // "0" is used to ensure single digits have trailing zeros
        r = "0" + Math.floor(r).toString(16);
        g = "0" + Math.floor(g).toString(16);
        b = "0" + Math.floor(b).toString(16);

        // Append in format "#rrggbb"
        colors.push('#'
            + r.substring(r.length - 2, r.length)
            + g.substring(g.length - 2, g.length)
            + b.substring(b.length - 2, b.length));
    }
    return colors;
}

/**
 * Specialised modulo function which only wraps when the numerator is greater than the denomenator
 * rather than when they are equal or greater.
 */
function specialMod(numerator, denomenator) {
    let result = numerator % denomenator;
    return result === 0 ? denomenator : result;
}

/**
 * Generate random positive integer within given range using given generator (max exclusive)
 */
function generate(min, max, rng) {
    return Math.floor(Math.max(rng() * max, min))
}

function generateHash(s) {
    let hash = 0;
    if (s.length === 0) {
        return hash;
    }
    for (let i = 0; i < s.length; i++) {
        let char = s.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return hash;
}

/**
 * Add contents of object b to object a (overriding contents of a where appropriate)
 * @param {Object} a Main object being updated
 * @param {Object} b Secondary object from which values will be read
 * @param {Array.<String>|null} path Recursive history of keys
 */
function merge(a, b, path=null) {
    if (path === null) {
        path = []
    }
    for (let key in b) {
        if (a.hasOwnProperty(key)) {
            if (a[key] instanceof Object && b[key] instanceof Object) {
                merge(a[key], b[key], path + [key.toString()]);
            } else if (a[key] !== b[key]) {
                a[key] = b[key];
            }
        } else {
            a[key] = b[key];
        }
    }
}
