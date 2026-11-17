'use client';

import { useState } from 'react';
import { ChoiceGroup, FileField } from '@/components/forms/Field';
import { useDictionary } from '@/i18n/LocaleProvider';

export function FormDemos() {
  const t = useDictionary().proposal;
  const [stage, setStage] = useState<string | string[]>('design');
  const [files, setFiles] = useState<File[]>([]);
  return (
    <>
      <ChoiceGroup
        legend={t.stage}
        name="sg-stage"
        value={stage}
        onChange={setStage}
        options={Object.entries(t.stages).map(([value, label]) => ({ value, label }))}
      />
      <FileField label={t.attachments} files={files} onFiles={setFiles} accept=".pdf" multiple />
    </>
  );
}
