import "../index.css";
import "../modules/draw/propagator/Propagator.css";

import _ from "lodash";
import { useCallback, useEffect, useState, useRef } from "react";
import { Tldraw, TldrawApp } from "tldraw";
import castInput from "../../modules/draw/propagator/castInput";
import deepDiff from "../../modules/draw/propagator/deepDiff";
import { Analytics } from "@vercel/analytics/react";

// Define types for records and editor
type RecordType = {
  id: string;
  type: string;
  typeName: string;
  props: {
    text?: string;
    geo?: string;
    start?: { boundShapeId: string };
    end?: { boundShapeId: string };
  };
};

type EditorType = {
  store: {
    allRecords: () => RecordType[];
    update: (id: string, updater: (record: RecordType) => RecordType) => void;
    listen: (
      callback: (change: ChangeType) => void,
      options: { source: string; scope: string }
    ) => () => void;
  };
};

type ChangeType = {
  changes: {
    added: Record<string, RecordType>;
    updated: Record<string, [RecordType, RecordType]>;
    removed: Record<string, RecordType>;
  };
};

export default function Propagator() {
  return (
    <div style={{ display: "flex", width: "100%" }}>
      <Tldraw onMount={setAppToState} persistenceKey="holograph-1" />
      <Analytics />
    </div>
  );
}