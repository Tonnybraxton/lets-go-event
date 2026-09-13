import { Module } from "@nestjs/common";
import { EventsModule } from "./modules/events/events.module.js";
import { HealthModule } from "./modules/health/health.module.js";

@Module({ imports: [HealthModule, EventsModule] })
export class AppModule {}
