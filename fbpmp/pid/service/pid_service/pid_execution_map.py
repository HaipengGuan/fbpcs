#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from fbpmp.pid.entity.pid_instance import PIDProtocol, PIDRole
from fbpmp.pid.entity.pid_stages import PIDFlowUnsupportedError, UnionPIDStage
from fbpmp.pid.service.pid_service.pid_flow_structs import (
    PIDExecutionFlowLookupKey,
    PIDFlow,
)


UnionPIDPublisherFlow = PIDFlow(
    name="union_pid_publisher",
    base_flow="union_pid",
    extra_args={},
    flow={
        UnionPIDStage.PUBLISHER_SHARD: [
            UnionPIDStage.PUBLISHER_PREPARE,
        ],
        UnionPIDStage.PUBLISHER_PREPARE: [UnionPIDStage.PUBLISHER_RUN_PID],
        UnionPIDStage.PUBLISHER_RUN_PID: [],
    },
)

UnionPIDAdvertiserFlow = PIDFlow(
    name="union_pid_advertiser",
    base_flow="union_pid",
    extra_args={},
    flow={
        UnionPIDStage.ADV_SHARD: [
            UnionPIDStage.ADV_PREPARE,
        ],
        UnionPIDStage.ADV_PREPARE: [UnionPIDStage.ADV_RUN_PID],
        UnionPIDStage.ADV_RUN_PID: [],
    },
)


# For now the only options supported are the union pid with publisher and partner roles
PIDDispatcherFlowMap = {
    PIDExecutionFlowLookupKey(
        PIDRole.PUBLISHER, PIDProtocol.UNION_PID
    ): UnionPIDPublisherFlow,
    PIDExecutionFlowLookupKey(
        PIDRole.PARTNER, PIDProtocol.UNION_PID
    ): UnionPIDAdvertiserFlow,
}


def get_execution_flow(role: PIDRole, protocol: PIDProtocol) -> PIDFlow:
    execution_key = PIDExecutionFlowLookupKey(role, protocol)
    try:
        return PIDDispatcherFlowMap[execution_key]
    except KeyError:
        raise PIDFlowUnsupportedError(
            f"Unsupported role/protocol combination: role={role}, protocol={protocol}."
        )