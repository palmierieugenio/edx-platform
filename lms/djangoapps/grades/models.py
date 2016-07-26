from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

from xmodule_django.models import BlockTypeKeyField, CourseKeyField, UsageKeyField

class PersistentSubsectionGrade(TimeStampedModel):
    """
    A django model tracking persistent grades at the subsection level.

    TODO: intended query patterns are fluid at the moment, document them here as they're firmed up.
    """

    class Meta(object):
        # TODO: these are also quite fluid as we nail down query patterns. Leaving single entries here for now to
        # facilitate planning, move them to field declarations once finalized.
        index_together = [
            ['user_id', 'course_id', 'content_type', 'is_valid'],
            ['user_id', 'content_id'],
            ['course_id', 'updated'],
            ['updated'],
        ]

        # TODO: are these the best uniqueness constraints? Is "A user has exactly one grade per subsection" a safe assumption?
        unique_together = (('user_id', 'content_id'))


    subtree_edited_date = models.DateTimeField('last content edit timestamp')

    # TODO: is this the right way to store course edit version? make sure it matches up w/ what Nimisha's exposing in her PR
    course_version = models.CharField('guid of latest course version', max_length=255)

    user = models.ForeignKey(User)  # CAUTION: FK may not exist in the future
    course_id = CourseKeyField(max_length=255)
    content_id = UsageKeyField(max_length=255)
    content_type = models.CharField('used to bucket grades by item type', max_length=255)

    # TODO: discussion on how many/which of these grades fields to include
    earned_grade = models.IntegerField()  # number of problems attempted and answered correctly
    max_earned_grade = models.IntegerField()  # number of problems attempted
    not_yet_attempted_grade = models.IntegerField()  # number of problems not yet attempted
    max_grade = models.IntegerField()  # always equal to max_earned_grade + not_yet_attempted_grade

    #is_valid = models.BinaryField()  # Might be needed if doing async updates

    visible_blocks = models.ForeignKey(BlockRecord)

class BlockRecord(models.Model):
    """
    A django model used to track the state of a block when used for grade calculation.
    """
    block_type = BlockTypeKeyField(max_length=255)
    block_id = UsageKeyField(max_length=255)
    block_version = models.IntegerField()
    visible_blocks = models.TextField()
    # TODO: hash for visible_blocks?
