from __future__ import annotations

import json
import os
import unittest
import warnings
from pathlib import Path
from typing import Any

import yaml

from checkov.common.checks_infra.checks_parser import NXGraphCheckParser
from checkov.common.checks_infra.registry import Registry
from checkov.common.models.enums import CheckResult
from checkov.runner_filter import RunnerFilter
from checkov.terraform import checks
from checkov.terraform.runner import Runner


class TestYamlPolicies(unittest.TestCase):
    def setUp(self) -> None:
        os.environ['UNIQUE_TAG'] = ''
        warnings.filterwarnings("ignore", category=ResourceWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    def test_ADORepositoryHasMinTwoReviewers(self):
        self.go("ADORepositoryHasMinTwoReviewers")

    def test_CodecommitApprovalRulesAttached(self):
        self.go("CodecommitApprovalRulesAttached")

    def test_RepositoryHasBranchProtection(self):
        self.go("RepositoryHasBranchProtection")

    def test_VPCHasFlowLog(self):
        self.go("VPCHasFlowLog")

    def test_VPCHasRestrictedSG(self):
        self.go("VPCHasRestrictedSG")

    def test_APIGWLoggingLevelsDefinedProperly(self):
        self.go("APIGWLoggingLevelsDefinedProperly")

    def test_GuardDutyIsEnabled(self):
        self.go("GuardDutyIsEnabled")

    def test_SGAttachedToResource(self):
        self.go("SGAttachedToResource")

    def test_StorageContainerActivityLogsNotPublic(self):
        self.go("StorageContainerActivityLogsNotPublic")

    def test_StorageCriticalDataEncryptedCMK(self):
        self.go("StorageCriticalDataEncryptedCMK")

    def test_VAconfiguredToSendReports(self):
        self.go("VAconfiguredToSendReports")

    def test_VAconfiguredToSendReportsToAdmins(self):
        self.go("VAconfiguredToSendReportsToAdmins")

    def test_VAisEnabledInStorageAccount(self):
        self.go("VAisEnabledInStorageAccount")

    def test_VAsetPeriodicScansOnSQL(self):
        self.go("VAsetPeriodicScansOnSQL")

    def test_CloudFrontHasResponseHeadersPolicy(self):
        self.go("CloudFrontHasResponseHeadersPolicy")

    def test_CloudtrailHasCloudwatch(self):
        self.go("CloudtrailHasCloudwatch")

    def test_S3BucketHasPublicAccessBlock(self):
        self.go("S3BucketHasPublicAccessBlock")

    def test_AccessToPostgreSQLFromAzureServicesIsDisabled(self):
        self.go("AccessToPostgreSQLFromAzureServicesIsDisabled")

    def test_AzureActiveDirectoryAdminIsConfigured(self):
        self.go("AzureActiveDirectoryAdminIsConfigured")

    def test_DisableAccessToSqlDBInstanceForRootUsersWithoutPassword(self):
        self.go("DisableAccessToSqlDBInstanceForRootUsersWithoutPassword")

    def test_GCPProjectHasNoLegacyNetworks(self):
        self.go("GCPProjectHasNoLegacyNetworks")

    def test_AzureDataFactoriesEncryptedWithCustomerManagedKey(self):
        self.go("AzureDataFactoriesEncryptedWithCustomerManagedKey")

    def test_AzureUnattachedDisksAreEncrypted(self):
        self.go("AzureUnattachedDisksAreEncrypted")

    def test_AzureNetworkInterfacePublicIPAddressId(self):
        self.go("AzureNetworkInterfacePublicIPAddressId")

    def test_AzureAntimalwareIsConfiguredWithAutoUpdatesForVMs(self):
        self.go("AzureAntimalwareIsConfiguredWithAutoUpdatesForVMs")

    def test_ALBRedirectsHTTPToHTTPS(self):
        self.go("ALBRedirectsHTTPToHTTPS")

    def test_GCPLogBucketsConfiguredUsingLock(self):
        self.go("GCPLogBucketsConfiguredUsingLock")

    def test_GCPAuditLogsConfiguredForAllServicesAndUsers(self):
        self.go("GCPAuditLogsConfiguredForAllServicesAndUsers")

    def test_GCPKMSCryptoKeysAreNotPubliclyAccessible(self):
        self.go("GCPKMSCryptoKeysAreNotPubliclyAccessible")

    def test_VirtualMachinesUtilizingManagedDisks(self):
        self.go("VirtualMachinesUtilizingManagedDisks")

    def test_RDSClusterHasBackupPlan(self):
        self.go("RDSClusterHasBackupPlan")

    def test_EBSAddedBackup(self):
        self.go("EBSAddedBackup")

    def test_AMRClustersNotOpenToInternet(self):
        self.go("AMRClustersNotOpenToInternet")

    def test_AutoScallingEnabledELB(self):
        self.go("AutoScallingEnabledELB")

    def test_IAMGroupHasAtLeastOneUser(self):
        self.go("IAMGroupHasAtLeastOneUser")

    def test_IAMUserHasNoConsoleAccess(self):
        self.go("IAMUserHasNoConsoleAccess")

    def test_IAMUsersAreMembersAtLeastOneGroup(self):
        self.go("IAMUsersAreMembersAtLeastOneGroup")

    def test_DataExplorerEncryptionUsesCustomKey(self):
        self.go("DataExplorerEncryptionUsesCustomKey")

    def test_MSQLenablesCustomerManagedKey(self):
        self.go("MSQLenablesCustomerManagedKey")

    def test_PGSQLenablesCustomerManagedKey(self):
        self.go("PGSQLenablesCustomerManagedKey")

    def test_StorageLoggingIsEnabledForBlobService(self):
        self.go("StorageLoggingIsEnabledForBlobService")

    def test_StorageLoggingIsEnabledForTableService(self):
        self.go("StorageLoggingIsEnabledForTableService")

    def test_VMHasBackUpMachine(self):
        self.go("VMHasBackUpMachine")

    def test_SubnetHasACL(self):
        self.go("SubnetHasACL")

    def test_GKEClustersAreNotUsingDefaultServiceAccount(self):
        self.go("GKEClustersAreNotUsingDefaultServiceAccount")

    def test_AzureStorageAccountsUseCustomerManagedKeyForEncryption(self):
        self.go("AzureStorageAccountsUseCustomerManagedKeyForEncryption")

    def test_AzureMSSQLServerHasSecurityAlertPolicy(self):
        self.go("AzureMSSQLServerHasSecurityAlertPolicy")

    def test_AzureSynapseWorkspacesHaveNoIPFirewallRulesAttached(self):
        self.go("AzureSynapseWorkspacesHaveNoIPFirewallRulesAttached")

    def test_EncryptedEBSVolumeOnlyConnectedToEC2s(self):
        self.go("EncryptedEBSVolumeOnlyConnectedToEC2s")

    def test_ServiceAccountHasGCPmanagedKey(self):
        self.go("ServiceAccountHasGCPmanagedKey")

    def test_AutoScalingEnableOnDynamoDBTables(self):
        self.go("AutoScalingEnableOnDynamoDBTables")

    def test_EIPAllocatedToVPCAttachedEC2(self):
        self.go("EIPAllocatedToVPCAttachedEC2")

    def test_EFSAddedBackup(self):
        self.go("EFSAddedBackup")

    def test_EFSAddedBackupSuppress(self):
        self.go("EFSAddedBackupSuppress", "EFSAddedBackup")

    def test_Route53ARecordAttachedResource(self):
        self.go("Route53ARecordAttachedResource")

    def test_PostgresRDSHasQueryLoggingEnabled(self):
        self.go("PostgresRDSHasQueryLoggingEnabled")

    def test_HTTPNotSendingPasswords(self):
        self.go("HTTPNotSendingPasswords")

    def test_PostgresDBHasQueryLoggingEnabled(self):
        self.go("PostgresDBHasQueryLoggingEnabled")

    def test_ALBProtectedByWAF(self):
        self.go("ALBProtectedByWAF")

    def test_APIProtectedByWAF(self):
        self.go("APIProtectedByWAF")

    def test_SQLServerAuditingEnabled(self):
        self.go("SQLServerAuditingEnabled")

    def test_WAF2HasLogs(self):
        self.go("WAF2HasLogs")

    def test_AppSyncProtectedByWAF(self):
        self.go("AppSyncProtectedByWAF")

    def test_SQLServerAuditingRetention90Days(self):
        self.go("SQLServerAuditingRetention90Days")

    def test_AWSSSMParameterShouldBeEncrypted(self):
        self.go("AWSSSMParametershouldbeEncrypted", "AWSSSMParameterShouldBeEncrypted")

    def test_AWSNATGatewaysshouldbeutilized(self):
        self.go("AWSNATGatewaysshouldbeutilized")

    def test_GCPKMSKeyRingsAreNotPubliclyAccessible(self):
        self.go("GCPKMSKeyRingsAreNotPubliclyAccessible")

    def test_GCPContainerRegistryReposAreNotPubliclyAccessible(self):
        self.go("GCPContainerRegistryReposAreNotPubliclyAccessible")

    def test_S3BucketVersioning(self):
        self.go("S3BucketVersioning")

    def test_S3PublicACLRead(self):
        self.go("S3PublicACLRead")

    def test_S3PublicACLWrite(self):
        self.go("S3PublicACLWrite")

    def test_S3BucketEncryption(self):
        self.go("S3BucketEncryption")

    def test_S3BucketLogging(self):
        self.go("S3BucketLogging")

    def test_AdministratorUserNotAssociatedWithAPIKey(self):
        self.go("AdministratorUserNotAssociatedWithAPIKey")

    def test_ApplicationGatewayEnablesWAF(self):
        self.go("ApplicationGatewayEnablesWAF")

    def test_S3KMSEncryptedByDefault(self):
        self.go("S3KMSEncryptedByDefault")

    def test_S3BucketReplicationConfiguration(self):
        self.go("S3BucketReplicationConfiguration")

    def test_AppLoadBalancerTLS12(self):
        self.go("AppLoadBalancerTLS12")

    def test_registry_load(self):
        registry = Registry(parser=NXGraphCheckParser(), checks_dir=str(
            Path(__file__).parent.parent.parent.parent.parent / "checkov" / "terraform" / "checks" / "graph_checks"))
        registry.load_checks()
        self.assertGreater(len(registry.checks), 0)

    def go(self, dir_name: str, check_name: str | None = None) -> None:
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                f"resources/{dir_name}")
        check_name = dir_name if check_name is None else check_name
        assert os.path.exists(dir_path)
        policy_dir_path = os.path.dirname(checks.__file__)
        assert os.path.exists(policy_dir_path)
        found = False
        for root, d_names, f_names in os.walk(policy_dir_path):
            for f_name in f_names:
                if f_name == f"{check_name}.yaml":
                    found = True
                    policy = load_yaml_data(f_name, root)
                    assert policy is not None
                    expected = load_yaml_data("expected.yaml", dir_path)
                    assert expected is not None
                    report = get_policy_results(dir_path, policy)
                    expected = load_yaml_data("expected.yaml", dir_path)

                    expected_to_fail = expected.get('fail', [])
                    expected_to_pass = expected.get('pass', [])
                    expected_to_skip = expected.get('skip', [])

                    self.assert_entities(expected_to_pass, report.passed_checks, True)
                    self.assert_entities(expected_to_fail, report.failed_checks, False)
                    self.assert_entities(expected_to_skip, report.skipped_checks, True)

        assert found

    def assert_entities(self, expected_entities: list[str], results: list[CheckResult], assertion: bool) -> None:
        self.assertEqual(len(expected_entities), len(results),
                         f"mismatch in number of results in {'passed' if assertion else 'failed'}, "
                         f"expected: {len(expected_entities)}, got: {len(results)}")
        for expected_entity in expected_entities:
            found = False
            for check_result in results:
                entity_id = check_result.resource
                if entity_id == expected_entity:
                    found = True
                    break
            self.assertTrue(found, f"expected to find entity {expected_entity}, {'passed' if assertion else 'failed'}")


def get_policy_results(root_folder, policy):
    check_id = policy['metadata']['id']
    graph_runner = Runner()
    report = graph_runner.run(root_folder, runner_filter=RunnerFilter(checks=[check_id]))
    return report


def wrap_policy(policy):
    policy['query'] = policy['definition']
    del policy['definition']


def load_yaml_data(source_file_name: str, dir_path: str) -> dict[str, Any] | None:
    expected_path = os.path.join(dir_path, source_file_name)
    if not os.path.exists(expected_path):
        return None

    with open(expected_path, "r") as f:
        expected_data = yaml.safe_load(f)

    return json.loads(json.dumps(expected_data))

    def test_Route53ZoneEnableDNSSECSigning(self):
        self.go("Route53ZoneEnableDNSSECSigning")

    def test_Route53ZoneHasMatchingQueryLog(self):
        self.go("Route53ZoneHasMatchingQueryLog")