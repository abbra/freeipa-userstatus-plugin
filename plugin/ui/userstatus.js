define([
        'freeipa/phases',
        'freeipa/ipa'],
        function(phases, IPA) {

// helper function
function get_item(array, attr, value) {

    for (var i=0,l=array.length; i<l; i++) {
        if (array[i][attr] === value) return array[i];
    }
    return null;
}

var userstatus_plugin = {};

// adds 'inetuserstatus' field into user details facet
userstatus_plugin.add_user_status_pre_op = function() {

    var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
    var section = get_item(facet.sections, 'name', 'misc');
    section.fields.push({
                            $type: 'radio',
                            name: 'inetuserstatus',
                            flags: ['w_if_no_aci'],
                            options: [
                                { label: '@i18n:userstatus.status_active', value: 'active' },
                                { label: '@i18n:userstatus.status_inactive', value: 'inactive' },
                                { label: '@i18n:userstatus.status_disabled', value: 'disabled' }
                            ],
                            tooltip: {
                                title: '@i18n:userstatus.user_tooltip',
                                html: true
                            },
    });
    return true;
};

phases.on('customization', userstatus_plugin.add_user_status_pre_op);

return userstatus_plugin;
});

