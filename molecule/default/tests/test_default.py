"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution == "fedora":
        pkgs = ["make", "rpm-build", "amazon-ssm-agent"]
    elif distribution == "debian" or distribution == "ubuntu" or distribution == "kali":
        pkgs = ["make", "binutils", "amazon-ssm-agent"]
    elif distribution == "amzn":
        pkgs = ["amazon-ssm-agent"]
    else:
        # We don't support this distribution
        assert False
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


@pytest.mark.parametrize("service", ["amazon-ssm-agent"])
def test_services(host, service):
    """Test that the expected services were enabled."""
    assert host.service(service).is_enabled
