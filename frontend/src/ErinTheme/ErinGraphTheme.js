import { assign } from "lodash";

// *
// * Colors
// *
const yellow = "#ffe119";
const orange = "#f58231";
const pink = "#fabebe";
const lavender = "#e6beff";
const maroon = "#800000";
const navy = "#000075";
const blue = "#4363d8";
const grey = "#a9a9a9";
const white = "#ffffff";
const black = "#000000";
const colors = [yellow,blue, orange, maroon, lavender, pink, navy];
// *
// * Typography
// *
const sansSerif = "'Roboto', 'Helvetica Neue', Helvetica, sans-serif";
const letterSpacing = "normal";
const fontSize = 12;
// *
// * Layout
// *
const padding = 8;
const baseProps = {
    width: 450,
    height: 300,
    padding: {top:10, bottom:50, left:50, right:50}
};
// *
// * Labels
// *
const baseLabelStyles = {
    fontFamily: sansSerif,
    fontSize,
    letterSpacing,
    padding,
    fill: white,
    stroke: "transparent",
    strokeWidth: 0
};

// *
// * Strokes
// *
const strokeDasharray = "10, 5";
const strokeLinecap = "round";
const strokeLinejoin = "round";

export default {
    area: assign(
        {
            style: {
                data: {
                    fill: black
                },
                labels: baseLabelStyles
            }
        },
        baseProps
    ),
    axis: assign(
        {
            style: {
                axis: {
                    fill: "transparent",
                    stroke: grey,
                    strokeWidth: 2,
                    strokeLinecap,
                    strokeLinejoin
                },
                grid: {
                    fill: "none",
                    stroke: blue,
                    strokeDasharray,
                    strokeLinecap,
                    strokeLinejoin,
                    pointerEvents: "painted"
                },
                ticks: {
                    fill: "transparent",
                    size: 5,
                    stroke: grey,
                    strokeWidth: 1,
                    strokeLinecap,
                    strokeLinejoin
                },
            }
        },
        baseProps
    ),
    bar: assign(
        {
            style: {
                data: {
                    fill: white,
                    padding,
                    strokeWidth: 0
                },
                labels: baseLabelStyles
            }
        },
        baseProps
    ),
    boxplot: assign(
        {
            style: {
                max: { padding, stroke: white, strokeWidth: 1 },
                maxLabels: baseLabelStyles,
                median: { padding, stroke: white, strokeWidth: 1 },
                medianLabels: baseLabelStyles,
                min: { padding, stroke: white, strokeWidth: 1 },
                minLabels: baseLabelStyles,
                q1: { padding, fill: white },
                q1Labels: baseLabelStyles,
                q3: { padding, fill: white },
                q3Labels: baseLabelStyles
            },
            boxWidth: 20
        },
        baseProps
    ),
    candlestick: assign(
        {
            style: {
                data: {
                    stroke: white
                },
                labels: baseLabelStyles
            },
            candleColors: {
                positive: "#ffffff",
                negative: white
            }
        },
        baseProps
    ),
    chart: baseProps,
    errorbar: assign(
        {
            borderWidth: 8,
            style: {
                data: {
                    fill: "transparent",
                    opacity: 1,
                    stroke: white,
                    strokeWidth: 2
                },
                labels: baseLabelStyles
            }
        },
        baseProps
    ),
    group: assign(
        {
            colorScale: colors
        },
        baseProps
    ),
    legend: {
        colorScale: colors,
        gutter: 10,
        orientation: "vertical",
        titleOrientation: "top",
        style: {
            data: {
                type: "circle"
            },
            labels: baseLabelStyles,
            title: assign({}, baseLabelStyles, { padding: 5 })
        }
    },
    line: assign(
        {
            style: {
                data: {
                    fill: "transparent",
                    opacity: 1,
                    stroke: white,
                    strokeWidth: 1
                },
                labels: baseLabelStyles
            }
        },
        baseProps
    ),
    pie: assign(
        {
            colorScale: colors,
            style: {
                data: {
                    padding,
                    stroke: blue,
                    strokeWidth: 1
                },
                labels: assign({}, baseLabelStyles, { padding: 20 })
            }
        },
        baseProps
    ),
    scatter: assign(
        {
            style: {
                data: {
                    fill: white,
                    opacity: 1,
                    stroke: "transparent",
                    strokeWidth: 0,
                    size:1
                },
                labels: baseLabelStyles
            }
        },
        baseProps
    ),
    stack: assign(
        {
            colorScale: colors
        },
        baseProps
    ),
    tooltip: {
        style: assign({}, baseLabelStyles, { padding: 5, pointerEvents: "none" }),
        flyoutStyle: {
            stroke: black,
            strokeWidth: 1,
            fill: "#f0f0f0",
            pointerEvents: "none"
        },
        cornerRadius: 5,
        pointerLength: 10
    },
    voronoi: assign(
        {
            style: {
                data: {
                    fill: "transparent",
                    stroke: "transparent",
                    strokeWidth: 0
                },
                labels: assign({}, baseLabelStyles, { padding: 5, pointerEvents: "none" }),
                flyout: {
                    stroke: black,
                    strokeWidth: 1,
                    fill: "#f0f0f0",
                    pointerEvents: "none"
                }
            }
        },
        baseProps
    )
};