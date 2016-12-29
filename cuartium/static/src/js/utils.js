var $ = require ('jquery');

module.exports = {

    escapeHTML: function (str) {
        return $('<div>').text(str).html();
    }

}
