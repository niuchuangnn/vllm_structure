from typing import List
from typing import Sequence as GenericSequence
from typing import Union

from vllm.sequence import PoolerOutput, SamplerOutput, SequenceGroupOutput


def create_output_by_sequence_group(
        outputs: GenericSequence[Union[SamplerOutput, PoolerOutput]],
        num_seq_groups: int) -> List[List[SequenceGroupOutput]]:
    """Helper method which transforms a 2d list organized by
    [step][sequence group] into [sequence group][step].
    """
    output_by_sequence_group: List[List[SequenceGroupOutput]] = [
        [] for _ in range(num_seq_groups)
    ]
    for step in outputs:
        for i, sequence_group_output in enumerate(step):
            output_by_sequence_group[i].append(sequence_group_output)

    return output_by_sequence_group


def create_template_output_by_sequence_group(
        outputs: GenericSequence[Union[SamplerOutput, PoolerOutput]],
        num_seq_groups: int) -> List[List[dict]]:
    """Helper method which transforms a 2d list organized by
    [step][sequence group] into [sequence group][step].
    """
    template_output_by_sequence_group: List[List[dict]] = [
        [] for _ in range(num_seq_groups)
    ]
    for step in outputs:
        for i in range(len(step.template_outputs)):
            template_output_by_sequence_group[i].append(step.template_outputs[i])

    return template_output_by_sequence_group
