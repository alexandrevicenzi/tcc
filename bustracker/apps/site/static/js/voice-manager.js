/*
    This module takes control of responsiveVoice.

    This module add a queue for messages.
    You can play many messages you want, and
    all will be played.
*/


var speaker = function (module) {
    /*
        Init the Speaker.
        Call this before everything.
    */
    module.init = function (options) {
        if(!responsiveVoice.voiceSupport()) {
            console.warn('Voice not supported!');
        } else {
            responsiveVoice.setDefaultVoice('Brazilian Portuguese Female');
        }

        module._queue = [];
    };

    module.play = function (message) {
        if(responsiveVoice.isPlaying()) {
            module._queue = module._queue.concat([message]);
        } else {
            responsiveVoice.speak(message, 'Brazilian Portuguese Female', { onend: module._nextMessage });
        }
    };

    module._nextMessage = function () {
        var message = module._queue.pop();
        if (message) {
            module.play(message);
        }
    };

    return module;
}({});