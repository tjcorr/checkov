#!/bin/bash

# Leverage the default env variables as described in:
# https://docs.github.com/en/actions/reference/environment-variables#default-environment-variables
if [[ $GITHUB_ACTIONS != "true" ]]
then
  checkov "$@"
  exit $?
fi

matcher_path=`pwd`/checkov-problem-matcher.json
warning_matcher_path=`pwd`/checkov-problem-matcher-softfail.json
cp /usr/local/lib/checkov-problem-matcher.json "$matcher_path"
cp /usr/local/lib/checkov-problem-matcher-softfail.json "$warning_matcher_path"

export BC_SOURCE=githubActions

# Actions pass inputs as $INPUT_<input name> environment variables
#
[[ -n "$INPUT_SKIP_CHECK" ]] && SKIP_CHECK_FLAG="--skip-check $INPUT_SKIP_CHECK"
[[ -n "$INPUT_FRAMEWORK" ]] && FRAMEWORK_FLAG="--framework $INPUT_FRAMEWORK"
[[ -n "$INPUT_OUTPUT_FORMAT" ]] && OUTPUT_FLAG="--output $INPUT_OUTPUT_FORMAT"
[[ -n "$INPUT_BASELINE" ]] && BASELINE_FLAG="--baseline $INPUT_BASELINE"
[[ -n "$INPUT_CONFIG_FILE" ]] && CONFIG_FILE_FLAG="--config-file $INPUT_CONFIG_FILE"
[[ -n "$INPUT_SOFT_FAIL_ON" ]] && SOFT_FAIL_ON_FLAG="--soft-fail-on $INPUT_SOFT_FAIL_ON"
[[ -n "$INPUT_HARD_FAIL_ON" ]] && HARD_FAIL_ON_FLAG="--hard-fail-on $INPUT_HARD_FAIL_ON"
[[ -n "$INPUT_VAR_FILE" ]] && VAR_FILE_FLAG="--var-file $INPUT_VAR_FILE"


if [ -n "$INPUT_COMPACT" ] && [ "$INPUT_COMPACT" = "true" ]; then
  COMPACT_FLAG="--compact"
fi

if [ -n "$INPUT_QUIET" ] && [ "$INPUT_QUIET" = "true" ]; then
  QUIET_FLAG="--quiet"
fi

if [ -n "$INPUT_DOWNLOAD_EXTERNAL_MODULES" ] && [ "$INPUT_DOWNLOAD_EXTERNAL_MODULES" = "true" ]; then
  DOWNLOAD_EXTERNAL_MODULES_FLAG="--download-external-modules true"
fi

if [ -n "$INPUT_SOFT_FAIL" ] && [ "$INPUT_SOFT_FAIL" =  "true" ]; then
  SOFT_FAIL_FLAG="--soft-fail"
fi

if [ -n "$INPUT_USE_ENFORCEMENT_RULES" ] && [ "$INPUT_USE_ENFORCEMENT_RULES" =  "true" ]; then
  USE_ENFORCEMENT_RULES_FLAG="--use-enforcement-rules"
fi

if [ -n "$INPUT_LOG_LEVEL" ]; then
  export LOG_LEVEL=$INPUT_LOG_LEVEL
fi

EXTCHECK_DIRS_FLAG=""
if [ -n "$INPUT_EXTERNAL_CHECKS_DIRS" ]; then
  IFS=', ' read -r -a extchecks_dir <<< "$INPUT_EXTERNAL_CHECKS_DIRS"
  for d in "${extchecks_dir[@]}"
  do
    EXTCHECK_DIRS_FLAG="$EXTCHECK_DIRS_FLAG --external-checks-dir $d"
  done
fi

CHECK_FLAG=""
if [ -n "$INPUT_CHECK" ]; then
  IFS=', ' read -r -a checks <<< "$INPUT_CHECK"
  for d in "${checks[@]}"
  do
    CHECK_FLAG="$CHECK_FLAG --check $d"
  done
fi

EXTCHECK_REPOS_FLAG=""
if [ -n "$INPUT_EXTERNAL_CHECKS_REPOS" ]; then
  IFS=', ' read -r -a extchecks_git <<< "$INPUT_EXTERNAL_CHECKS_REPOS"
  for repo in "${extchecks_git[@]}"
  do
    EXTCHECK_REPOS_FLAG="$EXTCHECK_REPOS_FLAG --external-checks-git $repo"
  done
fi

if [[ -z "$INPUT_SOFT_FAIL" ]]; then
    echo "::add-matcher::checkov-problem-matcher.json"
else
    echo "::add-matcher::checkov-problem-matcher-softfail.json"
fi

API_KEY=${API_KEY_VARIABLE}

GIT_BRANCH=${GITHUB_HEAD_REF:="$GITHUB_REF_NAME"}
GIT_BRANCH=${GIT_BRANCH:=master}
export BC_FROM_BRANCH=${GIT_BRANCH}
export BC_TO_BRANCH=${GITHUB_BASE_REF}
export BC_PR_ID=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')
export BC_PR_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/pull/${BC_PR_ID}"
export BC_COMMIT_HASH=${GITHUB_SHA}
export BC_COMMIT_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/commit/${GITHUB_SHA}"
export BC_AUTHOR_NAME=${GITHUB_ACTOR}
export BC_AUTHOR_URL="${GITHUB_SERVER_URL}/${BC_AUTHOR_NAME}"
export BC_RUN_ID=${GITHUB_RUN_NUMBER}
export BC_RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
export BC_REPOSITORY_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}"

echo "BC_FROM_BRANCH=${GIT_BRANCH}"
echo "BC_TO_BRANCH=${GITHUB_BASE_REF}"
echo "BC_PR_ID=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')"
echo "BC_PR_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/pull/${BC_PR_ID}""
echo "BC_COMMIT_HASH=${GITHUB_SHA}"
echo "BC_COMMIT_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/commit/${GITHUB_SHA}""
echo "BC_AUTHOR_NAME=${GITHUB_ACTOR}"
echo "BC_AUTHOR_URL="${GITHUB_SERVER_URL}/${BC_AUTHOR_NAME}""
echo "BC_RUN_ID=${GITHUB_RUN_NUMBER}"
echo "BC_RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}""
echo "BC_REPOSITORY_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}""

# If Docker image is used, default to that
if [ -n "$INPUT_DOCKER_IMAGE" ]; then
  DOCKER_IMAGE_FLAG="--docker-image $INPUT_DOCKER_IMAGE"
  DOCKERFILE_PATH_FLAG="--dockerfile-path $INPUT_DOCKERFILE_PATH"
  echo "checkov --bc-api-key <API_KEY> --branch $GIT_BRANCH --repo-id $GITHUB_REPOSITORY $DOCKER_IMAGE_FLAG $DOCKERFILE_PATH_FLAG"
  CHECKOV_RESULTS=$(checkov --bc-api-key $API_KEY_VARIABLE --branch $GIT_BRANCH --repo-id $GITHUB_REPOSITORY $DOCKER_IMAGE_FLAG $DOCKERFILE_PATH_FLAG)
# Else if File Variable exists then use -f flag to scan specific resources
else
  if [ -n "$INPUT_FILE" ]; then
    RESOURCE_TO_SCAN="-f $INPUT_FILE"
    echo "running checkov on file: $INPUT_FILE"
  else
  # Otherwise exists then use -d flag for directory scanning
    RESOURCE_TO_SCAN="-d $INPUT_DIRECTORY"
    echo "running checkov on directory: $INPUT_DIRECTORY"
  fi 
  # Build command
  if [ -n "$API_KEY_VARIABLE" ]; then
    echo "checkov --bc-api-key XXXXXXXXX-XXX-XXXXX --branch $GIT_BRANCH --repo-id $GITHUB_REPOSITORY $RESOURCE_TO_SCAN $CHECK_FLAG $SKIP_CHECK_FLAG $COMPACT_FLAG $QUIET_FLAG $SOFT_FAIL_FLAG $USE_ENFORCEMENT_RULES_FLAG $EXTCHECK_DIRS_FLAG $EXTCHECK_REPOS_FLAG $OUTPUT_FLAG $DOWNLOAD_EXTERNAL_MODULES_FLAG $CONFIG_FILE_FLAG $SOFT_FAIL_ON_FLAG $HARD_FAIL_ON_FLAG $FRAMEWORK_FLAG $BASELINE_FLAG $VAR_FILE_FLAG"
    CHECKOV_RESULTS=$(checkov --bc-api-key $API_KEY_VARIABLE --branch $GIT_BRANCH --repo-id $GITHUB_REPOSITORY $RESOURCE_TO_SCAN $CHECK_FLAG $SKIP_CHECK_FLAG $COMPACT_FLAG $QUIET_FLAG $SOFT_FAIL_FLAG $USE_ENFORCEMENT_RULES_FLAG $EXTCHECK_DIRS_FLAG $EXTCHECK_REPOS_FLAG $OUTPUT_FLAG $DOWNLOAD_EXTERNAL_MODULES_FLAG $CONFIG_FILE_FLAG $SOFT_FAIL_ON_FLAG $HARD_FAIL_ON_FLAG $FRAMEWORK_FLAG $BASELINE_FLAG $VAR_FILE_FLAG)
    else
    echo "checkov $RESOURCE_TO_SCAN $CHECK_FLAG $SKIP_CHECK_FLAG $COMPACT_FLAG $QUIET_FLAG $EXTCHECK_DIRS_FLAG $EXTCHECK_REPOS_FLAG $OUTPUT_FLAG $SOFT_FAIL_FLAG $USE_ENFORCEMENT_RULES_FLAG $DOWNLOAD_EXTERNAL_MODULES_FLAG $CONFIG_FILE_FLAG $SOFT_FAIL_ON_FLAG $HARD_FAIL_ON_FLAG $FRAMEWORK_FLAG $BASELINE_FLAG $VAR_FILE_FLAG"
    CHECKOV_RESULTS=$(checkov $RESOURCE_TO_SCAN $CHECK_FLAG $SKIP_CHECK_FLAG $COMPACT_FLAG $QUIET_FLAG $EXTCHECK_DIRS_FLAG $EXTCHECK_REPOS_FLAG $OUTPUT_FLAG $SOFT_FAIL_FLAG $USE_ENFORCEMENT_RULES_FLAG $DOWNLOAD_EXTERNAL_MODULES_FLAG $CONFIG_FILE_FLAG $SOFT_FAIL_ON_FLAG $HARD_FAIL_ON_FLAG $FRAMEWORK_FLAG $BASELINE_FLAG $VAR_FILE_FLAG)
  fi
fi

CHECKOV_EXIT_CODE=$?

CHECKOV_RESULTS="${CHECKOV_RESULTS//$'\\n'/''}"

{ echo "CHECKOV_RESULTS<<EOF"; echo "${CHECKOV_RESULTS:0:65536}"; echo "EOF"; } >> $GITHUB_ENV
{ echo "results<<EOF"; echo "$CHECKOV_RESULTS"; echo "EOF"; } >> $GITHUB_OUTPUT

if [ -n "$INPUT_DOWNLOAD_EXTERNAL_MODULES" ] && [ "$INPUT_DOWNLOAD_EXTERNAL_MODULES" = "true" ]; then
  echo "Cleaning up $INPUT_DIRECTORY/.external_modules directory"
  #This directory must be removed here for the self hosted github runners run as non-root user.
  rm -fr $INPUT_DIRECTORY/.external_modules
  exit $CHECKOV_EXIT_CODE
fi
exit $CHECKOV_EXIT_CODE
