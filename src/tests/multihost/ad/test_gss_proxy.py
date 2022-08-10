""" AD-Provider - GSS Proxy tests for bugzillas

:requirement: gss_proxy
:casecomponent: sssd
:subsystemteam: sst_idm_sssd
:upstream: yes
"""
import time
import tempfile
import pytest

from sssd.testlib.common.utils import sssdTools


@pytest.mark.tier1_3
@pytest.mark.gss_proxy
class TestGSSProxy:
    """ Miscellaneous Automated Test Cases for AD integration Bugzillas"""

    @staticmethod
    def test_0001_gss_proxy_parameter(
            multihost, adjoin, create_aduser_group):
        """
        :title: IDM-SSSD-TC: Test GSS Proxy feature
        :bugzilla:
        :id:
        :setup:
          1.Configure sssd with AD provider.
          2.Edit /etc/sysconfig/sssd to contain GSS_USE_PROXY=no
        :steps:
          1.Start SSSD
          2.Search SSSD logs to ensure GSS API is being used
        :expectedresults:
          1.Logs contain GSS Proxy messages
        """

        adjoin(membersw='adcli')
        hostname = multihost.client[0].run_command(
            'hostname -s', raiseonerr=False).stdout_text.rstrip().upper()

        # Create AD user and group
        (aduser, _) = create_aduser_group

        # Configure sssd
        client = sssdTools(multihost.client[0], multihost.ad[0])
        client.backup_sssd_conf()

        dom_section = f'domain/{client.get_domain_section_name()}'
        sssd_params = {
            'ad_domain': multihost.ad[0].domainname,
            'krb5_realm': multihost.ad[0].domainname.upper(),
            'realmd_tags': 'manages-system joined-with-adcli',
            'cache_credentials': 'True',
            'id_provider': 'ad',
            'krb5_store_password_if_offline': 'True',
            'default_shell': '/bin/bash',
            'ldap_sasl_authid': f'{hostname}$',
            'ldap_id_mapping': 'False',
            'use_fully_qualified_names': 'False',
            'fallback_homedir': '/home/%u',
            'access_provider': 'simple',
            'debug_level': '9',
        }
        client.sssd_conf(dom_section, sssd_params)
    
        multihost.client[0].run_command('cp -rf /etc/sysconfig/sssd '
                                        '/etc/sysconfig/sssd.bak')
        multihost.client[0].run_command('echo \"GSS_USE_PROXY=no\" '
                                        '>> /etc/sysconfig/sssd')

        client.clear_sssd_cache()
        time.sleep(5)

        # Download the sssd domain log
        log_str = multihost.client[0].get_file_contents(
            f"/var/log/sssd/sssd_{multihost.ad[0].domainname.lower()}.log"). \
            decode('utf-8')
        
        multihost.client[0].run_command(
            f"cat /var/log/sssd/sssd_{multihost.ad[0].domainname.lower()}.log")

        client.restore_sssd_conf()
        client.clear_sssd_cache()

#        assert "gss" in log_str
