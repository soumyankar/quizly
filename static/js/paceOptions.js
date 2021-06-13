 window.paceOptions = {
    startOnLoadPage: true,
    restartOnPushState: true,
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
    },
    restartOnRequestAfter: 50
}

Pace.on("start", function(){
    console.log("Pace starts.")
    $('.page_overlay').delay(50).fadeIn(150);
});


Pace.on("done", function(){
    console.log("pace stops.");
    $('.page_overlay').delay(300).fadeOut(600);
});

