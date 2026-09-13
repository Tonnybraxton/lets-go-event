import { Module } from "@nestjs/common";
import { EventsController } from "./events.controller.js";
import { EventsService, locationProvider } from "./events.service.js";

@Module({ controllers: [EventsController], providers: [EventsService, locationProvider], exports: [EventsService] })
export class EventsModule {}
