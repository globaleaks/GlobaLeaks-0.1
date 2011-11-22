def translate():
    return "jQuery(document).ready(function(){jQuery('body').translate('%s');});" % request.args(0).split('.')[0]

