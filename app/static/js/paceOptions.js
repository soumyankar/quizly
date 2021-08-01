 window.paceOptions = {
    startOnLoadPage: true,
    restartOnPushState: true,
    restartOnRequestAfter: true,
    minTime: 250,
    ghostTime: 100,
    easeFactor: 1.25,
    maxProgressPerFrame: 20,
    target: 'body',
    // Only show the progress on regular and ajax-y page navigation, not every request
    eventLag: {
        minSamples: 10,
        sampleCount: 3,
        lagThreshold: 3
    }
}
