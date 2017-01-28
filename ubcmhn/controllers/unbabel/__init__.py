from ubcmhn.controllers.base import BaseController

from ubcmhn.util.unbabelsimpleapi import UnbabelSimpleApi
from ubcmhn.util.hnwrappers import ItemTranslationStatus, TrFieldsByHnItem


class UnbabelTranslationController(BaseController):
    def init(self):
        self.ubapi = UnbabelSimpleApi(self.config.UBUN, self.config.UBAK, sandbox=True)

        self.source_language = self.config.SRCLANG
        self.translation_targets = (self.config.DSTLANG1, self.config.DSTLANG2)

    def FindUntranslatedItems(self):

        retval = {}

        for lang in self.translation_targets:
            retval[lang] = (list(self.db.get_untranslated_stories(lang)),
                            list(self.db.get_untranslated_comments(lang)))

        return retval

    def RequestTranslation(self, hnitemid, targetlang):
        l = self.l()
        ubapi = self.ubapi
        db = self.db

        # Get item
        hnitem = self.db.get_itembyhnid(hnitemid)

        if hnitem['deleted']:
            self.l().error("Item {0} is DELETED, skipping...".format(hnitemid))
            return

        # Get item translation status for targetlang
        status = ItemTranslationStatus(hnitem, targetlang)
        if status != "untranslated":
            self.l().warning("Item {0} has status \"{1}\", skipping translation request.".format(hnitemid,
                                                                                                 status))
            return

        ##################
        # Request Translation
        ##################
        origfield, translatedfield, unbabeltrjobfield = TrFieldsByHnItem(hnitem, targetlang)

        if not hnitem[origfield]:
            # Text field is blank for this id!?
            self.l().error("Item {0} has BLANK TEXT (fieldname={1}). skipping...".format(hnitemid, origfield))
            return

        transjob_response = ubapi.post_translation(hnitem[origfield], source_language=self.source_language,
                                                                      target_language=targetlang)

        if transjob_response:
            # Translation has been requested -- Get Unbabel job uid
            unbabeljobuid = transjob_response['uid']

            # Update items fields to reflect just-asked translation attempt.
            hnitem[unbabeltrjobfield] = transjob_response

            # Upsert item to the Database
            self.db.upsert_item(hnitem)


    def FindRequestedTranslations(self):

        retval = {}

        for lang in self.translation_targets:
            retval[lang] = list(self.db.get_translationrequested_items(lang))

        return retval

    def FetchTranslation(self, hnitemid, targetlang):
        l = self.l()
        ubapi = self.ubapi
        db = self.db

        # Get item
        hnitem = self.db.get_itembyhnid(hnitemid)

        # Get item translation status for targetlang
        status = ItemTranslationStatus(hnitem, targetlang)
        if status != "processing":
            self.l().warning("Item {0} has status \"{1}\", skipping fetch-translation request.".format(
                                                                                                hnitemid,
                                                                                                status))
            return

        ##################
        # Fetch Translation
        ##################
        origfield, translatedfield, unbabeltrjobfield = TrFieldsByHnItem(hnitem, targetlang)

        # Get Unbabel JOB UID from hnitem
        unbabeljobuid = hnitem[unbabeltrjobfield]['uid']

        fetchtransjob_response = ubapi.get_translation(unbabeljobuid)

        if fetchtransjob_response:
            jobstatus = fetchtransjob_response['status']
            # Translation job has been fetched -- Check if translation happened!
            if jobstatus == 'completed':
                # Translation is OK! Get text and updated translated field.
                translated_text = fetchtransjob_response['translatedText']

                # Update Item
                hnitem[translatedfield] = translated_text
                hnitem[unbabeltrjobfield] = fetchtransjob_response

                # Upsert it!
                self.db.upsert_item(hnitem)
                self.l().warning("Translation OK!!!! ITEM={0}".format(hnitemid))
                return hnitem
            else:
                # Translation is not completed! Skipping...
                self.l().warning("Translation ITEM={0} UBJOBUID={1} STATUS={2}. Skipping...".format(
                                                                                    hnitemid,
                                                                                    unbabeljobuid,
                                                                                    jobstatus
                                                                                    ))
                return None
