var App = (function () {
    var remotePostProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };

    var remotePutProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'PUT',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };

    var remoteDeleteProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'DELETE',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };

    var remoteGetProcessing = function (url, data, defaultCallback, failureCallback) {
        $.get(url, JSON.stringify(data), defaultCallback).fail(failureCallback).done();
    };

    return {
        remotePost: function (url, data, defaultCallback, failureCallback) {
            return remotePostProcessing(url, data, defaultCallback, failureCallback);
        },
        remotePut: function (url, data, defaultCallback, failureCallback) {
            return remotePutProcessing(url, data, defaultCallback, failureCallback);
        },
        remoteDelete: function (url, data, defaultCallback, failureCallback) {
            return remoteDeleteProcessing(url, data, defaultCallback, failureCallback);
        },
        remoteGet: function (url, data, defaultCallback, failureCallback) {
            return remoteGetProcessing(url, data, defaultCallback, failureCallback)
        },
        showProcessing: function (options) {
            var options = $.extend(true, {}, options);
            var html = '<i class="fa fa-spinner fa-pulse fa-4x fa-fw"></i>';

            if (options.target) { // element blocking
                var el = $(options.target);
                if (el.height() <= ($(window).height())) {
                    options.cenrerY = true;
                }
                el.block({
                    message: html,
                    baseZ: options.zIndex ? options.zIndex : 1000,
                    centerY: options.cenrerY !== undefined ? options.cenrerY : false,
                    css: {
                        top: '10%',
                        border: '0',
                        padding: '0',
                        backgroundColor: 'none'
                    },
                    overlayCSS: {
                        backgroundColor: options.overlayColor ? options.overlayColor : '#555',
                        opacity: options.boxed ? 0.05 : 0.1,
                        cursor: 'wait'
                    }
                });
            } else { // page blocking
                $.blockUI({
                    message: html,
                    baseZ: options.zIndex ? options.zIndex : 1000,
                    css: {
                        border: '0',
                        padding: '0',
                        backgroundColor: 'none'
                    },
                    overlayCSS: {
                        backgroundColor: options.overlayColor ? options.overlayColor : '#555',
                        opacity: options.boxed ? 0.05 : 0.1,
                        cursor: 'wait'
                    }
                });
            }
        },
        hideProcessing: function (target) {
            if (target) {
                $(target).unblock({
                    onUnblock: function () {
                        $(target).css('position', '');
                        $(target).css('zoom', '');
                    }
                });
            } else {
                $.unblockUI();
            }
        },
        notifyUser: function (message, message_type, position) {
            var position = position || 'right';
            var message_type = message_type || 'success';
            $.notify(message, {position: position, className: message_type});
        },
        confirmAlert: function (message, okCallback) {

        },
        redirectTo: function (path, timeout) {
            if (timeout)
                setTimeout(function () {
                    window.location.href = path
                }, timeout);
            else
                window.location.href = path
        },
        getUrlParameterByName: function (name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                results = regex.exec(location.search);
            return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        }
    }
})();