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

    packages = None
    snaps = None
    if distribution in ["amzn", "debian", "fedora", "kali"]:
        packages = ["amazon-ssm-agent"]
    elif distribution in ["ubuntu"]:
        packages = ["snapd"]
        snaps = ["amazon-ssm-agent"]
    else:
        raise ValueError(f"Unknown distribution {distribution}")

    assert all(host.package(pkg).is_installed for pkg in packages)

    if distribution in ["ubuntu"]:
        assert all(host.run(f"snap list {snap}").rc == 0 for snap in snaps)


@pytest.mark.parametrize("service", ["amazon-ssm-agent"])
def test_services(host, service):
    """Test that the expected services were enabled."""
    distribution = host.system_info.distribution

    services = None
    snap_services = None
    if distribution in ["amzn", "debian", "fedora", "kali"]:
        services = ["amazon-ssm-agent"]
    elif distribution in ["ubuntu"]:
        services = ["snapd.service", "snap.amazon-ssm-agent.amazon-ssm-agent.service"]
        snap_services = ["amazon-ssm-agent"]
    else:
        raise ValueError(f"Unknown distribution {distribution}")

    assert all(host.service(svc).is_enabled for svc in services)

    if distribution in ["ubuntu"]:
        assert all(host.run(f"snap services {svc}").rc == 0 for svc in snap_services)
