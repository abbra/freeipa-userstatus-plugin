#
# A demo file to demonstrate how client-side plugin could amend IPA commands
# Example below is taken straight from freeIPA core where '--out' in user_show
# is overridden to allow saving a user certificate to a file.
#
# It has no relation to userstatus plugin at all and is provided for demo purposes only
#
# from ipaclient.frontend import MethodOverride
# from ipalib import errors
# from ipalib import Flag
# from ipalib import util
# from ipalib.plugable import Registry
# from ipalib import _
# from ipalib import x509
#
# @register(override=True, no_fail=True)
# class user_show(MethodOverride):
#     def forward(self, *keys, **options):
#         if 'out' in options:
#             util.check_writable_file(options['out'])
#             result = super(user_show, self).forward(*keys, **options)
#             if 'usercertificate' in result['result']:
#                 certs = (x509.load_der_x509_certificate(c)
#                          for c in result['result']['usercertificate'])
#                 x509.write_certificate_list(certs, options['out'])
#                 result['summary'] = (
#                     _('Certificate(s) stored in file \'%(file)s\'')
#                     % dict(file=options['out'])
#                 )
#                 return result
#             else:
#                 raise errors.NoCertificateError(entry=keys[-1])
#         else:
#             return super(user_show, self).forward(*keys, **options)


