# ###############################################################
#
# extract the name of the RPM pacakge from source.
# The B2SAFE version number is extracted from rulebase/local.re
#
# usage:
# -----
# rpm {BUILD}
#
# return:
# irods-eudat-b2safe-${MAJOR_VERS}.${MINOR_VERS}.${SUB_VERS}-${BUILD}.noarch.rpm
#
# ###############################################################
function rpm_package()
{
    local BUILD=$1
    local ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
    local MAJOR_VERS=`grep "^\s*\*major_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
    local MINOR_VERS=`grep "^\s*\*minor_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
    local SUB_VERS=`grep "^\s*\*sub_version" $ABSOLUTE_PATH/../rulebase/local.re | awk -F\" '{print $2}'`
    local VERSION="${MAJOR_VERS}.${MINOR_VERS}.${SUB_VERS}"
    echo "irods-eudat-b2safe-${MAJOR_VERS}.${MINOR_VERS}.${SUB_VERS}-${BUILD}.noarch.rpm"
}

# ###############################################################
#
# usage:
# -----
# irods_version {OS_VERSION}_{IRODS_VERSION}
#
# return irods-version
#
# example:
# -------
# irods_version centos7_4_2_6
# > 4.2.6
#
# ###############################################################
function irods_version()
{
    local VERSION=$1
    echo $VERSION | awk 'BEGIN{ FS="_"; }{ print $2"."$3"."$4; }'
}

# ###############################################################
#
# usage:
# -----
# repo_name VERSION GIT_URL GIT_BRANCH
#
# VERSION: {OS_VERSION}_{IRODS_VERSION}, e.g. centos7_4_2_6
# GIT_URL: git repository
# GIT_BRANCH: name of the branch to be build
#
# return:
# ------
# irods-${IRODS_VERSION}                (if user is EUDAT-B2SAFE and
#                                        BRANCH is master)
# {USER}/{BRANCH}/irods-${IROS_VERSION} (otherwise)
#
# examples:
# --------
#  soruce version.sh
#  repo_name centos7_4_2_1 https://github.com/B2SAFE-CORE/B2SAFE-core master
#   > irods-4.2.1
#  repo_name centos7_4_2_1 https://github.com/B2SAFE-CORE/B2SAFE-core devel
#   > B2SAFE-CORE/devel/irods-4.2.1
#  repo_name centos7_4_2_1 https://github.com/stefan-wolfsheimer/B2SAFE-core master
#   > stefan-wolfsheimer/master/irods-4.2.1
# ###############################################################
function repo_name()
{
    local VERSION=$1
    local GIT_URL=$2
    local GIT_BRANCH=$3
    local IRODS_VERSION=$( echo $VERSION | awk 'BEGIN{ FS="_"; }{ print $2"."$3"."$4; }' )
    local USER=$( echo $GIT_URL | awk 'BEGIN{ FS="/"; }{ print $4; }' )
    if [[ "${USER}" == "EUDAT-B2SAFE" ]] && [[ "${GIT_BRANCH}" == "master" ]]
    then
        echo irods-${IRODS_VERSION}
    else
        echo "${USER}/${GIT_BRANCH}/irods-${IRODS_VERSION}"
    fi
}
