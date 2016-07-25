from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

from xmodule_django.models import BlockTypeKeyField, CourseKeyField, UsageKeyField

class PersistentSubsectionGradeModel(TimeStampedModel):
    """
    A django model tracking persistent grades at the subsection level.

    TODO: intended query patterns are fluid at the moment, document them here as they're firmed up.
    """

    class Meta(object):
        index_together = [
            # TODO: nail down indices as we flesh out the API layer
        ]

        unique_together = (('user_id', 'course_id', 'block_type', 'block_id'))


    subtree_edited_date = models.DateTimeField('last content edit timestamp')
    user = models.ForeignKey(User)  # CAUTION: FK may not exist in the future
    earned_grade = models.IntegerField()
    max_grade = models.IntegerField()
    visible_blocks = models.ForeignKey(BlockRecord)

    # TODO: Make sure this matches up w/ what Nimisha's exposing in her PR
    course_version = models.CharField('guid of latest course version', max_length=255)

    # These 3 are essentially a deconstructed UsageKey
    course_id = CourseKeyField(max_length=255)
    block_type = BlockTypeKeyField(max_length=255)
    block_id = models.CharField(max_length=255)  # TODO: CharField correct here?

    #is_valid = models.BinaryField()  # Might be needed if doing async updates


class BlockRecord(models.Model):
    """
    A django model used to track the state of a block when used for grade calculation.
    """
    block_type = BlockTypeKeyField(max_length=255)
    block_id = CharField(max_length=255)
    visible_blocks = models.TextField()
    visible_hash = models.CharField(max_length=255)  # TODO: ensure this calculation is done in a performant way
