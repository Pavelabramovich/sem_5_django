import difflib
import pprint
from unittest.util import safe_repr, _common_shorten_repr


class AssertNestedSequencesEqualsMixin:
    def assertNestedSequencesEquals(self, seq1, seq2, msg=None):
        if standardMsg := self.__get_fail_message(seq1, seq2):
            diffMsg = '\n' + '\n'.join(
                difflib.ndiff(pprint.pformat(seq1).splitlines(),
                              pprint.pformat(seq2).splitlines()))

            standardMsg = self._truncateMessage(standardMsg, diffMsg)
            msg = self._formatMessage(msg, standardMsg)
            self.fail(msg)

    @classmethod
    def __get_fail_message(cls, obj1, obj2):
        if obj1 == obj2:
            return None

        seq1 = obj1
        seq2 = obj2

        seq_type_name = "sequence"
        differing = []

        try:
            len1 = len(seq1)
        except (TypeError, NotImplementedError):
            differing.append(f'First {seq_type_name} has no length.    Non-sequence?')

        try:
            len2 = len(seq2)
        except (TypeError, NotImplementedError):
            differing.append(f'Second {seq_type_name} has no length.    Non-sequence?')

        if len(differing) == 2:
            differing = f"{seq1} != {seq2}\n"

        elif len(differing) == 1:
            differing = differing[0]

        else:
            if seq1 == seq2:
                return

            first, second = _common_shorten_repr(seq1, seq2)
            differing = f'{seq_type_name.capitalize()}s differ: {first} != {second}\n'

            for i in range(min(len1, len2)):
                try:
                    item1 = seq1[i]
                except (TypeError, IndexError, NotImplementedError):
                    differing += f'\nUnable to index element {i} of first {seq_type_name}\n'
                    break

                try:
                    item2 = seq2[i]
                except (TypeError, IndexError, NotImplementedError):
                    differing += f'\nUnable to index element {i} of second {seq_type_name}\n'
                    break

                item_differing = cls.__get_fail_message(item1, item2)

                if item_differing:
                    differing += f'\nFirst differing element {i}:\n' + item_differing
                    break
            else:
                if len1 == len2:
                    return

            if len1 > len2:
                differing += f'\nFirst {seq_type_name} contains {len1 - len2} additional '
                try:
                    differing += f'First extra element {len2}:\n{safe_repr(seq1[len2])}\n'

                except (TypeError, IndexError, NotImplementedError):
                    differing += f'Unable to index element {len2}  of first {seq_type_name}\n'

            elif len1 < len2:
                differing += f'\nSecond {seq_type_name} contains {len2 - len1} additional '
                try:
                    differing += f'Second extra element {len1}:\n{safe_repr(seq2[len1])}\n'

                except (TypeError, IndexError, NotImplementedError):
                    differing += f'Unable to index element {len1}  of first {seq_type_name}\n'

        return differing
